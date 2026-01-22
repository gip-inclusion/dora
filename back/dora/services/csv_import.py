import csv
import logging
import sys
from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Union

from django.db import IntegrityError, transaction
from django.db.models import QuerySet
from django.utils import timezone

from dora.admin_express.models import AdminDivisionType, City
from dora.admin_express.utils import arrdt_to_main_insee_code
from dora.core.utils import get_geo_data, skip_csv_lines
from dora.services.enums import ServiceStatus
from dora.services.models import (
    FundingLabel,
    LocationKind,
    Service,
    ServiceModel,
    ServiceSource,
)
from dora.services.utils import instantiate_service_from_model
from dora.structures.models import Structure
from dora.users.models import User

logger = logging.getLogger(__name__)


class ImportServicesHelper:
    def __init__(self) -> None:
        self.wet_run: bool = False
        self.importing_user: Optional[User] = None
        self.source: Optional[ServiceSource] = None

    def _initialize_trackers(self):
        self.geo_data_missing_lines: List[Dict[str, Union[int, str]]] = []
        self.draft_services_created: List[Dict[str, Union[int, str, List[str]]]] = []
        self.duplicated_services = []
        self.errors = []
        self.created_count = 0

    def import_services(
        self,
        reader: csv.reader,
        importing_user: User,
        source_info: dict[str, str],
        wet_run: bool = False,
        should_remove_first_two_lines: bool = False,
    ) -> Dict[str, Union[List[Any], int, List[str]]]:
        self.wet_run = wet_run
        self.importing_user = importing_user
        self._initialize_trackers()

        if self.wet_run:
            logger.info("⚠️ PRODUCTION RUN ⚠️")
        else:
            logger.info("🧘 DRY RUN 🧘")

        csv_reader = (
            skip_csv_lines(reader, 2) if should_remove_first_two_lines else reader
        )

        [headers, *lines] = csv_reader
        lines = [dict(zip(headers, line)) for line in lines]

        try:
            missing_headers = set(self.CSV_HEADERS) - set(headers)
            if missing_headers:
                logger.info(
                    "Les headers suivants sont manquants : (%s)",
                    ", ".join(missing_headers),
                )
                return {"missing_headers": list(missing_headers)}

            with transaction.atomic():
                if self.wet_run:
                    try:
                        self._get_service_source(source_info)
                    except IntegrityError as e:
                        logger.warning(
                            "Erreur critique: %s", source_info["value"], exc_info=e
                        )
                        return {
                            "errors": [
                                f'Le fichier nommé "{source_info["value"]}" a déjà un nom de source stocké dans le base de données. Veuillez refaire l\'import avec un nouveau nom de source.'
                            ]
                        }
                for idx, line in enumerate(lines, 2):
                    try:
                        logger.info(f"\nTraitement de la ligne {idx} :")

                        data = self._extract_data_from_line(line)

                        # Vérification que le SIRET de la structure est bien renseigné
                        if not data.structure_siret:
                            error_msg = f"[{idx}] SIRET manquant pour la structure."
                            logger.warning("❌ %s", error_msg)
                            self.errors.append(error_msg)
                            continue

                        # Vérification que la structure existe bien en BDD
                        try:
                            structure = Structure.objects.get(
                                siret=data.structure_siret
                            )
                        except Structure.DoesNotExist:
                            error_msg = f"[{idx}] Structure avec le SIRET {data.structure_siret} introuvable."
                            logger.warning("❌ %s", error_msg)
                            self.errors.append(error_msg)
                            continue

                        # Vérification que le modèle de service existe lui aussi
                        try:
                            model = ServiceModel.objects.get(slug=data.modele_slug)
                        except ServiceModel.DoesNotExist:
                            error_msg = f"[{idx}] Modèle de service avec le slug {data.modele_slug} introuvable."
                            logger.warning(
                                "❌ %s",
                                error_msg,
                            )
                            self.errors.append(error_msg)
                            continue

                        should_service_be_created = (
                            self._check_if_service_is_duplicated(data, idx)
                        )

                        if not should_service_be_created:
                            continue

                        logger.info(
                            "Création d'un nouveau service pour la structure avec le SIRET '%s'.",
                            data.structure_siret,
                        )
                        new_service = instantiate_service_from_model(
                            model, structure, self.importing_user
                        )
                        self._edit_and_save_service(
                            new_service,
                            data,
                            idx,
                        )

                        self.created_count += 1
                        logger.info("✅ Service créé.")

                    except Exception as e:
                        error_msg = f"[{idx}] {e}"
                        logger.warning("❌ %s", error_msg)
                        self.errors.append(error_msg)
                        continue

                if len(self.errors) > 0 and self.wet_run:
                    self.created_count = 0
                    raise Exception(
                        f"⚠️ {len(self.errors)} erreurs rencontrées lors du traitement du fichier CSV.\n"
                        "Toutes les modifications sont annulées."
                    )

                if not self.wet_run:
                    raise Exception(
                        "Mode dry-run activé. Toutes les modifications sont annulées."
                    )
        except Exception as e:
            if str(e) != "Mode dry-run activé. Toutes les modifications sont annulées.":
                print(f"\nErreur critique : {e}", file=sys.stderr)

        print("\n--------------------------------------------------")
        print("Traitement du fichier CSV terminé.")
        print(
            f"Résumé : {self.created_count} services créés, {len(self.errors)} erreurs."
        )
        print(
            f"Services potentiellement dupliqués : ({len(self.duplicated_services)}):"
        )
        print(f"Services en brouillon créés : ({len(self.draft_services_created)})")
        print(
            f"Lignes sans données géographiques : ({len(self.geo_data_missing_lines)})"
        )
        for entry in self.geo_data_missing_lines:
            print(
                f"Ligne {entry['idx']}: Adresse={entry['address']}, Ville={entry['city']}, "
                f"Code postal={entry['postal_code']}"
            )
        print("--------------------------------------------------\n")

        return {
            "created_count": self.created_count,
            "errors": self.errors,
            "geo_data_missing_lines": self.geo_data_missing_lines,
            "duplicated_services": self.duplicated_services,
            "draft_services_created": self.draft_services_created,
        }

    def _extract_multiple_values_from_line(
        self, line: Dict[str, str], header_name: str, model: Any, category_label: str
    ) -> QuerySet:
        values = [
            label.strip().strip(",")
            for label in line.get(header_name, "").split(",")
            if label.strip()
        ]

        if len(values) == 0:
            return []

        queryset = model.objects.filter(value__in=values)

        if queryset.count() != len(values):
            invalid_values = set(values) - set(queryset.values_list("value", flat=True))
            if len(invalid_values) > 0:
                raise ValueError(
                    f"Un ou plusieurs {category_label} sont introuvables : {invalid_values}.",
                )
            raise ValueError(
                f"Un ou plusieurs {category_label} sont dupliqués.",
            )

        return queryset

    def _extract_diffusion_zone_type_from_line(
        self, line: Dict[str, str]
    ) -> Union[AdminDivisionType, str]:
        diffusion_zone_type_raw = line.get("diffusion_zone_type", "").strip()
        if not diffusion_zone_type_raw:
            return ""

        for choice in AdminDivisionType:
            if diffusion_zone_type_raw == choice.value:
                return choice

        raise ValueError(
            f"Type de zone de diffusion avec la valeur '{diffusion_zone_type_raw}' introuvable.",
        )

    def _extract_data_from_line(self, line: Dict[str, str]) -> SimpleNamespace:
        data = SimpleNamespace(
            modele_slug=line.get("modele_slug").strip(),
            structure_siret=line.get("structure_siret").replace(" ", "").strip(),
            contact_name=line.get("contact_name").strip(),
            contact_email=line.get("contact_email").strip(),
            contact_phone=line.get("contact_phone").replace(" ", "").strip(),
            location_city=line.get("location_city").strip(),
            location_address=line.get("location_address").strip(),
            location_complement=line.get("location_complement").strip(),
            location_postal_code=line.get("location_postal_code")
            .replace(" ", "")
            .strip(),
            location_kinds=self._extract_multiple_values_from_line(
                line, "location_kinds", LocationKind, "types d'accueil"
            ),
            funding_labels=self._extract_multiple_values_from_line(
                line, "labels_financement", FundingLabel, "labels de financement"
            ),
            is_contact_info_public=line.get("is_contact_info_public", "").strip(),
            diffusion_zone_type=self._extract_diffusion_zone_type_from_line(line),
        )
        return data

    def _edit_and_save_service(
        self,
        service: Service,
        data: SimpleNamespace,
        idx: int,
    ) -> None:
        service.creator = self.importing_user
        service.last_editor = self.importing_user
        service.contact_name = data.contact_name
        service.contact_email = data.contact_email
        service.contact_phone = data.contact_phone
        service.address1 = data.location_address
        service.address2 = data.location_complement
        service.city = data.location_city
        service.postal_code = data.location_postal_code
        service.location_kinds.set(data.location_kinds)
        service.diffusion_zone_type = data.diffusion_zone_type
        service.is_contact_info_public = data.is_contact_info_public.lower() == "oui"

        service.source = self.source

        if service.address1 and service.city and service.postal_code:
            geo_data = get_geo_data(
                service.address1, city=service.city, postal_code=service.postal_code
            )
            if geo_data:
                service.city_code = geo_data.city_code
                service.geom = geo_data.geom
                service.diffusion_zone_details = self.get_diffusion_zone_details(
                    service
                )
            else:
                self.geo_data_missing_lines.append(
                    {
                        "idx": idx,
                        "address": service.address1,
                        "city": service.city,
                        "postal_code": service.postal_code,
                    }
                )

        if service.is_eligible_for_publishing():
            service.status = ServiceStatus.PUBLISHED
            service.publication_date = timezone.now()
        else:
            missing_fields = service.get_missing_properties_for_publishing()
            self.draft_services_created.append(
                {
                    "idx": idx,
                    "name": service.name,
                    "missing_fields": missing_fields,
                }
            )

        service.funding_labels.add(*data.funding_labels)

        service.save()

    def _get_service_source(self, source_info: Dict[str, str]) -> None:
        source, _ = ServiceSource.objects.get_or_create(
            value=source_info["value"],
            label=source_info["label"],
        )
        self.source = source

    def _check_if_service_is_duplicated(self, data: SimpleNamespace, idx: int) -> bool:
        base_filter = {
            "structure__siret": data.structure_siret,
            "model__slug": data.modele_slug,
            "contact_email": data.contact_email,
        }

        if not Service.objects.filter(**base_filter).exists():
            return True

        has_location_data = all([data.location_address, data.location_postal_code])

        full_filter = {
            **base_filter,
            "address1": data.location_address,
            "postal_code": data.location_postal_code,
        }

        if has_location_data and Service.objects.filter(**full_filter).exists():
            error_msg = (
                f'[{idx}] Le même service avec le modèle "{data.modele_slug}", le référent "{data.contact_email}" '
                f"et la même adresse existe déjà pour la structure "
                f'dont le Siret est "{data.structure_siret}".'
            )

            self.errors.append(error_msg)
            logger.warning(
                error_msg,
            )
            return False

        self.duplicated_services.append(
            {
                "idx": idx,
                "siret": data.structure_siret,
                "model_slug": data.modele_slug,
                "contact_email": data.contact_email,
            }
        )

        return True

    @staticmethod
    def get_diffusion_zone_details(service: Service):
        city_code = service.city_code

        insee_code = arrdt_to_main_insee_code(city_code)

        try:
            city = City.objects.get(code=insee_code)
        except City.DoesNotExist:
            logger.error(f"La ville dont le code est {city_code} n'existe pas")
            raise City.DoesNotExist

        if service.diffusion_zone_type == AdminDivisionType.DEPARTMENT:
            return city.department

        if service.diffusion_zone_type == AdminDivisionType.REGION:
            return city.region

        if service.diffusion_zone_type == AdminDivisionType.EPCI:
            return city.epci

        return city_code

    CSV_HEADERS = [
        "modele_slug",
        "structure_siret",
        "contact_email",
        "diffusion_zone_type",
        "labels_financement",
        "contact_name",
        "contact_phone",
        "location_kinds",
        "location_city",
        "location_address",
        "location_complement",
        "location_postal_code",
        "is_contact_info_public",
    ]
