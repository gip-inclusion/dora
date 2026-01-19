import logging
from typing import Optional

from django.db import transaction
from django.utils import timezone
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from dora.core.mixins import BaseImportAdminMixin
from dora.core.utils import skip_csv_lines
from dora.services.models import FundingLabel, Service
from dora.users.models import User

logger = logging.getLogger(__name__)


class LabelServicesHelper(BaseImportAdminMixin):
    CSV_HEADERS = ["service_url", "label"]

    def __init__(self):
        self.wet_run: bool = False
        self.labeler: Optional[User] = None

    def get_import_type_name(self):
        return "label_services"

    def get_import_helper(self):
        return self

    def get_import_method_name(self):
        return "label_services"

    def get_import_title(self):
        return "Labellisation de services"

    def get_csv_headers(self):
        return self.CSV_HEADERS

    def _initialize_trackers(self):
        self.errors = []
        self.services_labeled_count = 0

    def label_services(
        self,
        reader,
        labeler: User,
        source_info=None,
        wet_run=False,
        should_remove_first_two_lines=False,
    ):
        self.wet_run = wet_run
        self.labeler = labeler

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
                for idx, line in enumerate(lines, 2):
                    logger.info(f"\nTraitement de la ligne {idx} :")

                    service_url = line["service_url"]
                    label_name = line["label"]
                    slug = service_url.split("/")[-1]

                    has_error = False

                    try:
                        service = Service.objects.get(slug=slug)
                    except Service.DoesNotExist:
                        error_msg = (
                            f"[{idx}] Le service avec le slug '{slug}' n'existe pas."
                        )
                        logger.warning(error_msg)
                        self.errors.append(error_msg)
                        has_error = True

                    try:
                        label = FundingLabel.objects.get(label=label_name)
                    except FundingLabel.DoesNotExist:
                        error_msg = f"[{idx}] Le label de financement '{label_name}' n'existe pas."
                        logger.warning(error_msg)
                        self.errors.append(error_msg)
                        has_error = True

                    if has_error:
                        continue

                    service.funding_labels.add(label)

                    service.last_editor = self.labeler
                    service.modification_date = timezone.now()
                    service.save()

                    logger.info(
                        "Le label de financement %s a été ajouté au service avec le slug %s.",
                        label_name,
                        slug,
                    )

                    self.services_labeled_count += 1

                if len(self.errors) > 0 and self.wet_run:
                    self.services_labeled_count = 0
                    raise Exception(
                        f"{len(self.errors)} erreurs rencontrées lors du traitement du fichier CSV.\n"
                        "Toutes les modifications sont annulées."
                    )

                if not self.wet_run:
                    raise Exception(
                        "Mode dry-run activé. Toutes les modifications sont annulées."
                    )

        except Exception as e:
            if str(e) != "Mode dry-run activé. Toutes les modifications sont annulées.":
                logger.error(f"\nErreur critique : {e}")

        return {
            "labeled_count": self.services_labeled_count,
            "errors": self.errors,
        }

    def format_results(self, result, is_wet_run):
        success_messages = []
        labeled_count = result.get("labeled_count", 0)
        missing_headers = result.get("missing_headers", [])
        errors = result.get("errors", [])

        no_errors = not missing_headers and not errors

        if missing_headers:
            return [
                {
                    "level": "error",
                    "message": format_html(
                        "<b>Échec de l'import - Colonnes manquantes</b><br/>Votre fichier CSV ne contient pas toutes les colonnes requises. Ajoutez les colonnes suivantes :<br/>{}",
                        format_html_join(
                            mark_safe("<br/>"), "• {}", ((h,) for h in missing_headers)
                        ),
                    ),
                }
            ]

        if errors:
            message_title = mark_safe(
                "Échec de l'import"
                if is_wet_run
                else "Test terminé - Erreurs à corriger"
            )
            message_text = mark_safe(
                "Aucun service n'a été labellisé, car le fichier comporte des erreurs."
                if is_wet_run
                else "Le fichier contient des erreurs qui empêcheront l'import."
            )
            return [
                {
                    "level": "error",
                    "message": format_html(
                        "<b>{}</b><br/>{} Veuillez corriger les éléments suivants :<br/>{}",
                        message_title,
                        message_text,
                        format_html_join(
                            mark_safe("<br/>"), "• {}", ((e,) for e in errors)
                        ),
                    ),
                }
            ]

        if is_wet_run and no_errors:
            success_messages.append(
                {
                    "level": "success",
                    "message": format_html(
                        "<b>Labellisation terminée avec succès</b><br/>{} services ont été labellisés",
                        labeled_count,
                    ),
                }
            )

        if not is_wet_run and no_errors:
            success_messages.append(
                {
                    "level": "success",
                    "message": format_html(
                        "<b>Test réalisé avec succès - aucune erreur détectée</b><br/>C'est tout bon ! {} services sont prêts à être labellisés.",
                        labeled_count,
                    ),
                }
            )

        return success_messages
