import logging
from typing import Optional

from django.db import transaction
from django.utils import timezone

from dora.core.utils import skip_csv_lines
from dora.services.models import FundingLabel, Service
from dora.users.models import User

logger = logging.getLogger(__name__)


class LabelServicesHelper:
    def __init__(self):
        self.wet_run: bool = False
        self.labeler: Optional[User] = None

    def _initialize_trackers(self):
        self.errors = []
        self.services_labeled_count = 0

    def label_services(
        self, reader, labeler: User, wet_run=False, should_remove_first_two_lines=False
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
                    try:
                        logger.info(f"\nTraitement de la ligne {idx} :")

                        service_url = line["service_url"]
                        label_name = line["label"]

                        label = FundingLabel.objects.get(label=label_name)

                        slug = service_url.split("/")[-1]
                        service = Service.objects.get(slug=slug)

                        service.funding_labels.add(label)

                        service.last_editor = self.labeler
                        service.modification_date = timezone.now()
                        service.save()

                        logger.info(
                            "Le label de financement %s a été ajouté au service avec le slug %s.",
                            label_name,
                            slug,
                        )

                    except FundingLabel.DoesNotExist:
                        error_msg = (
                            f"[{idx}] Le label de financement %s n'existe pas.",
                            label_name,
                        )
                        logger.warning(error_msg)
                        self.errors.append(error_msg)
                        continue

                    except Service.DoesNotExist:
                        error_msg = (
                            f"[{idx}] Le service avec le slug %s n'existe pas.",
                        )
                        logger.warning(error_msg)
                        self.errors.append(error_msg)
                        continue

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
            "created_count": self.services_labeled_count,
            "errors": self.errors,
        }

    CSV_HEADERS = ["service_url", "label"]
