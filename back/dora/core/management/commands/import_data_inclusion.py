import json
import logging

import requests
from data_inclusion.schema.v0 import TypologieStructure
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import Truncator
from furl import furl

from dora.core import utils
from dora.core.constants import WGS84
from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.services.models import (
    Credential,
    LocationKind,
    Public,
    Requirement,
    Service,
    ServiceCategory,
    ServiceFee,
    ServiceKind,
    ServiceSource,
    ServiceSubCategory,
)
from dora.sirene.models import Establishment
from dora.structures.models import Structure, StructureNationalLabel, StructureSource
from dora.users.models import User

logger = logging.getLogger(__name__)


# Documentation DI : https://data-inclusion-api-prod.osc-secnum-fr1.scalingo.io/api/v0/docs

BASE_URL = furl(settings.DATA_INCLUSION_URL)

STRUCTURES_INDEX = {}


def clean_field(value, max_length, default_value):
    if not value:
        return default_value
    return Truncator(value).chars(max_length)


class Command(BaseCommand):
    help = "Importe les nouvelles structures Data Inclusion qui n'existent pas encore dans Dora"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str)
        parser.add_argument("--department", type=str)

    def handle(self, *args, **options):
        department = options["department"]
        source = options["source"]

        if source.startswith("mediation-numerique"):
            self.stderr.write(
                self.style.ERROR("Source MedNum, utilisez `import_mednum`")
            )
            import sys

            sys.exit(-1)

        self.stdout.write(self.style.SUCCESS(f"Import de la source: {source}"))
        try:
            structures = self.get_structures(source, department)
            self.import_structures(source, structures)
            services = self.get_services(source, department)
            self.import_services(source, services)
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(e))

    def get_structures(self, source, department):
        structures = []
        args = {"source": source, "size": 100}
        if department:
            args["departement"] = department

        url = BASE_URL.copy().add(
            path="structures/",
            args=args,
        )

        for results in self.get_pages(url):
            structures += results

        return structures

    def get_services(self, source, department):
        services = []
        args = {"source": source, "size": 100}
        if department:
            args["departement"] = department

        url = BASE_URL.copy().add(
            path="services/",
            args=args,
        )

        for results in self.get_pages(url):
            services += results

        return services

    def get_pages(self, url):
        page = 1
        while True:
            paginated_url = url.copy().add({"page": page})
            self.stdout.write(f"Chargement de {paginated_url}")
            response = requests.get(
                paginated_url,
                params={},
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {settings.DATA_INCLUSION_IMPORT_API_KEY}",
                },
            )
            if response.status_code != 200:
                self.stderr.write(
                    self.style.ERROR(
                        f"Erreur dans la récupération des données\n{url}: {response.status_code}"
                    )
                )
                return

            result = json.loads(response.content)["items"]
            if len(result):
                yield result
                page += 1
            else:
                return

    def import_structures(self, source_value, structures):
        bot_user = User.objects.get_dora_bot()
        source, _created = StructureSource.objects.get_or_create(
            value=f"di-{source_value}",
            defaults={"label": source_value},
        )
        if _created:
            self.stdout.write(
                self.style.ERROR(
                    f"Source: di-{source_value} inexistante. Pensez à renseigner son label dans l'interface "
                    f"d'administration"
                )
            )
        num_imported = 0

        for s in structures:
            if not s["siret"]:
                continue
            STRUCTURES_INDEX[s["id"]] = s["siret"]

            if Structure.objects.filter(siret=s["siret"]).exists():
                continue
            try:
                establishment = Establishment.objects.get(siret=s["siret"])
            except Establishment.DoesNotExist:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Siret incorrect, ignoré : {s['siret']} ({s['nom']})"
                    )
                )
                continue
            try:
                structure = Structure.objects.create_from_establishment(establishment)
                structure.creator = bot_user
                structure.last_editor = bot_user
                structure.source = source
                structure.data_inclusion_id = s["id"]
                structure.data_inclusion_source = s["source"]
                structure.email = clean_field(s["courriel"], 254, "")
                structure.phone = utils.normalize_phone_number(s["telephone"] or "")
                structure.url = clean_field(s["site_web"], 200, "")
                structure.full_desc = s["presentation_detail"] or ""
                structure.short_desc = clean_field(s["presentation_resume"], 280, "")
                typo_di = s["typologie"]
                try:
                    typologie = TypologieStructure[typo_di]
                    structure.typology = typologie.value
                except KeyError:
                    logger.warning(
                        "La typologie “%s” n’est pas supportée",
                        typo_di,
                    )
                structure.accesslibre_url = s["accessibilite"]
                structure.save()

                for label in s["labels_nationaux"] or []:
                    new_label, _created = StructureNationalLabel.objects.get_or_create(
                        value=label
                    )
                    if _created:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Label national: {label} inexistant. Pensez à le compléter dans l'interface "
                                f"d'administration"
                            )
                        )
                    structure.national_labels.add(new_label)

                send_moderation_notification(
                    structure,
                    bot_user,
                    f"Structure importée de Data Inclusion ({source})",
                    ModerationStatus.VALIDATED,
                )
                num_imported += 1

            except Exception as e:
                print(s)
                self.stderr.write(s)
                self.stderr.write(self.style.ERROR(e))
        self.stdout.write(self.style.SUCCESS(f"{num_imported} structures importées"))

    def import_services(self, source_value, services):
        def cust_choice_to_objects(Model, values):
            if values:
                return Model.objects.filter(name__in=values)
            return []

        bot_user = User.objects.get_dora_bot()
        source, _created = ServiceSource.objects.get_or_create(
            value=f"di-{source_value}",
            defaults={"label": source_value},
        )
        if _created:
            self.stdout.write(
                self.style.ERROR(
                    f"Source: di-{source_value} inexistante. Pensez à renseigner son label dans l'interface "
                    f"d'administration"
                )
            )
        num_imported = 0
        for s in services:
            if Service.objects.filter(
                data_inclusion_id=s["id"],
                data_inclusion_source=s["source"],
            ).exists():
                continue
            siret = STRUCTURES_INDEX.get(s["structure_id"])
            if not siret:
                self.style.ERROR(f"Impossible de trouver le siret correspondant à {s}")
                continue
            structures = Structure.objects.filter(siret=siret)
            if not structures:
                self.stdout.write(
                    self.style.ERROR(
                        f"La structure correspondant au service {s['id']}, de siret {siret}, n'a pas été créée"
                    )
                )
                continue
            if len(structures) > 1:
                main_structures = structures.filter(parent=None)
                if main_structures:
                    structures = main_structures

            structure = structures[0]
            try:
                service = Service.objects.create(
                    data_inclusion_id=s["id"],
                    data_inclusion_source=s["source"],
                    structure=structure,
                    name=s["nom"],
                    short_desc=s["presentation_resume"] or "",
                    full_desc=s["presentation_detail"] or "",
                    fee_details=s["frais_autres"] or "",
                    is_cumulative=False if s["cumulable"] is False else True,
                    online_form=s["formulaire_en_ligne"] or "",
                    postal_code=s["code_postal"] or "",
                    city_code=s["code_insee"] or "",
                    address1=s["adresse"] or "",
                    address2=s["complement_adresse"] or "",
                    recurrence=s["recurrence"] or "",
                    suspension_date=s["date_suspension"],
                    contact_phone=utils.normalize_phone_number(s["telephone"]) or "",
                    contact_email=s["courriel"] or "",
                    is_contact_info_public=s["contact_public"] is True,
                    diffusion_zone_type=s["zone_diffusion_type"] or "",
                    diffusion_zone_details=s["zone_diffusion_code"] or "",
                    source=source,
                    creator=bot_user,
                    last_editor=bot_user,
                    modification_date=timezone.now(),
                )
                lon = s["longitude"]
                lat = s["latitude"]

                if lon and lat:
                    service.geom = Point(lon, lat, srid=WGS84)

                # TODO: à publier directement?
                # service.status = ServiceStatus.PUBLISHED
                # service.publication_date = timezone.now()

                service.publics.set(cust_choice_to_objects(Public, s["profils"]))
                service.requirements.set(
                    cust_choice_to_objects(Requirement, s["pre_requis"])
                )
                service.credentials.set(
                    cust_choice_to_objects(Credential, s["justificatifs"])
                )

                subcats = s["thematiques"]
                cats = [utils.get_category_from_subcategory(s) for s in subcats]
                service.categories.set(self._values_to_objects(ServiceCategory, cats))
                service.subcategories.set(
                    self._values_to_objects(ServiceSubCategory, subcats)
                )

                service.kinds.set(self._values_to_objects(ServiceKind, s["types"]))
                service.fee_condition = ServiceFee.objects.filter(
                    value__in=s["frais"]
                ).first()
                service.location_kinds.set(
                    self._values_to_objects(LocationKind, s["modes_accueil"])
                )

                service.save()
                send_moderation_notification(
                    service,
                    bot_user,
                    f"Structure importée de Data Inclusion ({source})",
                    ModerationStatus.VALIDATED,
                )
                num_imported += 1

            except Exception as e:
                print(e)
                print(s)
                self.stderr.write(s)
                self.stderr.write(self.style.ERROR(e))
                continue

        self.stdout.write(self.style.SUCCESS(f"{num_imported} services importés"))

    def _values_to_objects(self, Model, values):
        if values:
            return Model.objects.filter(value__in=values)
        return []
