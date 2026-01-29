import json

import requests
from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.utils.text import Truncator
from furl import furl

from dora.admin_express.models import AdminDivisionType
from dora.core import utils
from dora.core.commands import BaseCommand
from dora.core.constants import WGS84
from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.utils import code_insee_to_code_dept
from dora.data_inclusion.mappings import DI_TO_DORA_DIFFUSION_ZONE_TYPE_MAPPING
from dora.decoupage_administratif.models import City
from dora.services.enums import ServiceStatus
from dora.services.models import (
    BeneficiaryAccessMode,
    CoachOrientationMode,
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

# Documentation DI : https://data-inclusion-api-prod.osc-secnum-fr1.scalingo.io/api/v0/docs

BASE_URL = furl(settings.DATA_INCLUSION_URL)

STRUCTURES_INDEX = {}


def clean_field(value, max_length, default_value):
    if not value:
        return default_value
    return Truncator(value).chars(max_length)


def cust_choice_to_objects(Model, values):
    if values:
        return Model.objects.filter(name__in=values)
    return []


class Command(BaseCommand):
    help = "Importe les nouvelles structures Data Inclusion qui n'existent pas encore dans Dora"

    def add_arguments(self, parser):
        parser.add_argument("--department", type=str)

    def handle(self, *args, **options):
        department = options["department"]
        source = "mediation-numerique"

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

    def set_or_update_labels(self, structure, label_values):
        for label_value in label_values:
            label, _created = StructureNationalLabel.objects.get_or_create(
                value=label_value
            )
            if _created:
                self.stdout.write(
                    self.style.ERROR(
                        f"Label national: {label_value} inexistant. Pensez à le compléter dans l'interface "
                        f"d'administration"
                    )
                )
            if not structure.national_labels.filter(id=label.id).exists():
                structure.national_labels.add(label)

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

            STRUCTURES_INDEX[s["id"]] = (s["siret"], s["labels_nationaux"])

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
                structure.accesslibre_url = s["accessibilite"]
                structure.save()

                if s["labels_nationaux"]:
                    self.set_or_update_labels(structure, s["labels_nationaux"])

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
        existing_di_ids = Service.objects.filter(
            data_inclusion_source__startswith="mediation-numerique"
        ).values_list("data_inclusion_id", flat=True)
        existing_di_ids = [id for id in existing_di_ids if len(id) == 44]

        def already_imported(new_id):
            if Service.objects.filter(data_inclusion_id=new_id):
                return True
            # On gère les imports historiques aussi bien que possible
            # étant donné que les ids ont changé
            for id in new_id.split("__"):
                for existing_di_id in existing_di_ids:
                    if id.endswith(existing_di_id):
                        return True
            return False

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
            if already_imported(s["id"]):
                continue
            siret, labels_nationaux = STRUCTURES_INDEX.get(
                s["structure_id"], (None, [])
            )
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
                    diffusion_zone_type=DI_TO_DORA_DIFFUSION_ZONE_TYPE_MAPPING.get(
                        s["zone_diffusion_type"]
                    )
                    if s["zone_diffusion_type"]
                    else "",
                    diffusion_zone_details=s["zone_diffusion_code"] or "",
                    appointment_link=s["prise_rdv"] or "",
                    source=source,
                    creator=bot_user,
                    last_editor=bot_user,
                    modification_date=timezone.now(),
                )
                lon = s["longitude"]
                lat = s["latitude"]

                if lon and lat:
                    service.geom = Point(lon, lat, srid=WGS84)

                service.status = ServiceStatus.PUBLISHED
                service.publication_date = timezone.now()
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

                self._presave_mednum_services(service, labels_nationaux)

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

    def _presave_mednum_services(self, service, label_nationaux):
        service.use_inclusion_numerique_scheme = True

        if service.geom and not service.city_code:
            try:
                city = City.objects.get(geom__covers=service.geom)
            except City.DoesNotExist:
                self.stderr.write(self.style.ERROR("Impossible de déterminer la ville"))
            else:
                if city.code[:2] != service.postal_code[
                    :2
                ] and not service.postal_code.startswith("20"):
                    self.stderr.write(
                        self.style.ERROR("Ville inconsistente avec le code postal")
                    )
                else:
                    service.city_code = city.code

        if not service.diffusion_zone_type or not service.diffusion_zone_details:
            service.diffusion_zone_type = AdminDivisionType.DEPARTMENT
            if service.city_code:
                service.diffusion_zone_details = code_insee_to_code_dept(
                    service.city_code
                )

        service.coach_orientation_modes.add(
            CoachOrientationMode.objects.get(value="telephoner"),
            CoachOrientationMode.objects.get(value="envoyer-un-mail"),
        )

        service.beneficiaries_access_modes.add(
            BeneficiaryAccessMode.objects.get(value="telephoner"),
        )

        if not service.appointment_link:
            service.beneficiaries_access_modes.add(
                BeneficiaryAccessMode.objects.get(value="se-presenter"),
            )

        if label_nationaux:
            self.set_or_update_labels(service.structure, label_nationaux)
