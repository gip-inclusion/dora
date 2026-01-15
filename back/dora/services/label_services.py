import csv
import io
import logging
import threading
import traceback
from typing import Optional

from django.core.cache import cache
from django.db import transaction
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from dora.core.models import ImportJob
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

                        self.services_labeled_count += 1

                    except FundingLabel.DoesNotExist:
                        error_msg = f"[{idx}] Le label de financement '{label_name}' n'existe pas."
                        logger.warning(error_msg)
                        self.errors.append(error_msg)
                        continue

                    except Service.DoesNotExist:
                        error_msg = (
                            f"[{idx}] Le service avec le slug '{slug}' n'existe pas."
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
            "labeled_count": self.services_labeled_count,
            "errors": self.errors,
        }

    def handle_csv_upload(self, request):
        """Handle CSV upload for label services"""
        csv_file = request.FILES.get("csv_file")

        if not csv_file:
            return self._create_failed_job(
                request,
                "fichier-manquant.csv",
                "Veuillez sélectionner un fichier CSV.",
            )

        if not csv_file.name.lower().endswith(".csv"):
            return self._create_failed_job(
                request,
                csv_file.name,
                "<b>Échec de l'import - Format de fichier non valide</b><br/>"
                "Le fichier n'est pas au format CSV attendu. Assurez-vous d'utiliser un fichier .csv avec des colonnes séparées par des virgules.",
            )

        upload_size_limit = 50 * 1024 * 1024  # 50MB
        if csv_file.size > upload_size_limit:
            return self._create_failed_job(
                request,
                csv_file.name,
                "<b>Échec de l'import - Fichier trop volumineux</b><br/>Le fichier doit faire moins de 50 Mio.",
            )

        try:
            is_wet_run = request.POST.get("test_run") != "on"
            should_remove_instructions = (
                request.POST.get("should_remove_instructions") == "on"
            )

            csv_content = csv_file.read().decode("utf-8")

            import_job = ImportJob.objects.create(
                user=request.user,
                import_type="label_services",
                filename=csv_file.name,
                status="pending",
            )

            thread = threading.Thread(
                target=self._run_in_background,
                args=(
                    import_job.id,
                    csv_content,
                    request.user.id,
                    is_wet_run,
                    should_remove_instructions,
                ),
            )
            thread.daemon = True
            thread.start()

            return redirect(f"{request.path}?job_id={import_job.id}")

        except UnicodeDecodeError:
            return self._create_failed_job(
                request,
                csv_file.name,
                "<b>Échec de l'import - Erreur d'encodage du fichier</b><br/>"
                "Le fichier contient des caractères spéciaux illisibles. Sauvegardez votre fichier en UTF-8 et relancez l'import.",
            )
        except Exception as e:
            return self._create_failed_job(
                request,
                csv_file.name,
                f"<b>Échec de l'import - Erreur inattendue</b><br/>"
                f"L'erreur suivante s'est produite :<br/>"
                f"{e}<br/>"
                f"Si le problème persiste, contactez les développeurs.",
            )

    def _create_failed_job(self, request, filename, error_message):
        """Create a failed ImportJob for label services"""
        import_job = ImportJob.objects.create(
            user=request.user,
            import_type="label_services",
            filename=filename,
            status="failed",
        )

        cache_key = f"import_results:{import_job.id}"
        cache.set(
            cache_key,
            {"messages": [{"level": "error", "message": error_message}]},
            timeout=3600,  # 1 hour
        )

        return redirect(f"{request.path}?job_id={import_job.id}")

    def _run_in_background(
        self,
        job_id,
        csv_content,
        user_id,
        is_wet_run,
        should_remove_instructions,
    ):
        """Run label services import in background thread"""
        try:
            job = ImportJob.objects.get(id=job_id)
            job.status = "processing"
            job.started_at = timezone.now()
            job.save()

            user = User.objects.get(id=user_id)
            reader = csv.reader(io.StringIO(csv_content))

            result = self.label_services(
                reader,
                user,
                source_info=None,
                wet_run=is_wet_run,
                should_remove_first_two_lines=should_remove_instructions,
            )

            cache_key = f"import_results:{job_id}"
            cache.set(
                cache_key,
                {
                    "messages": self.format_results(result, is_wet_run),
                    "is_wet_run": is_wet_run,
                },
                timeout=3600,  # 1 hour
            )

            job.status = "completed"
            job.completed_at = timezone.now()
            job.save()

        except Exception as e:
            cache_key = f"import_results:{job_id}"
            cache.set(
                cache_key,
                {"error_message": f"{str(e)}\n\n{traceback.format_exc()}"},
                timeout=3600,  # 1 hour
            )

            job = ImportJob.objects.get(id=job_id)
            job.status = "failed"
            job.completed_at = timezone.now()
            job.save()

    def format_results(self, result, is_wet_run):
        """Format label services results for display"""
        success_messages = []
        labeled_count = result.get("labeled_count", 0)
        missing_headers = result.get("missing_headers", [])
        errors = result.get("errors", [])

        no_errors = not missing_headers and not errors

        # Missing headers
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

        # Errors
        if errors:
            message_title = mark_safe(
                "Échec de l'import" if is_wet_run else "Test terminé - Erreurs à corriger"
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

        # Success
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

    CSV_HEADERS = ["service_url", "label"]
