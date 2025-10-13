import csv
import io
import threading
import traceback

from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone

from dora.users.models import User

from .models import ImportJob

# Stockage temporaire des résultats de l'import
_import_results = {}


class BaseImportAdminMixin:
    upload_size_limit_in_bytes = 50 * 1024 * 1024  # 50MB to handle larger CSVs
    default_source_label = "DORA"

    def import_csv(self, request):
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

        if csv_file.size > self.upload_size_limit_in_bytes:
            return self._create_failed_job(
                request,
                csv_file.name,
                "<b>Échec de l'import - Fichier trop volumineux</b><br/>Le fichier doit faire moins de 50 Mio.",
            )

        try:
            is_wet_run = request.POST.get("test_run") != "on"
            source_label = request.POST.get(
                "source_label", self.default_source_label
            ).strip()
            should_remove_instructions_from_csv = (
                request.POST.get("should_remove_instructions") == "on"
            )

            csv_content = csv_file.read().decode("utf-8")

            import_job = ImportJob.objects.create(
                user=request.user,
                import_type=self.get_import_type_name(),
                filename=csv_file.name,
                status="pending",
            )

            source_info = {
                "value": csv_file.name.rsplit(".", 1)[0],
                "label": source_label or self.default_source_label,
            }

            # L'import va se passer dans un background thread pour empêcher un timeout
            thread = threading.Thread(
                target=self._run_import_in_background,
                args=(
                    import_job.id,
                    csv_content,
                    request.user.id,
                    source_info,
                    is_wet_run,
                    should_remove_instructions_from_csv,
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
        import_job = ImportJob.objects.create(
            user=request.user,
            import_type=self.get_import_type_name(),
            filename=filename,
            status="failed",
        )

        _import_results[str(import_job.id)] = {
            "messages": [{"level": "error", "message": error_message}],
        }

        return redirect(f"{request.path}?job_id={import_job.id}")

    def _run_import_in_background(
        self,
        job_id,
        csv_content,
        user_id,
        source_info,
        is_wet_run,
        should_remove_instructions,
    ):
        try:
            job = ImportJob.objects.get(id=job_id)
            job.status = "processing"
            job.started_at = timezone.now()
            job.save()

            user = User.objects.get(id=user_id)

            reader = csv.reader(io.StringIO(csv_content))

            helper = self.get_import_helper()
            method_name = self.get_import_method_name()
            import_method = getattr(helper, method_name)

            result = import_method(
                reader,
                user,
                source_info,
                wet_run=is_wet_run,
                should_remove_first_two_lines=should_remove_instructions,
            )

            _import_results[str(job_id)] = {
                "messages": self.format_results(result, is_wet_run),
                "is_wet_run": is_wet_run,
            }

            job.status = "completed"
            job.completed_at = timezone.now()
            job.save()

        except Exception as e:
            _import_results[str(job_id)] = {
                "error_message": f"{str(e)}\n\n{traceback.format_exc()}",
            }

            job = ImportJob.objects.get(id=job_id)
            job.status = "failed"
            job.completed_at = timezone.now()
            job.save()

    def get_import_helper(self):
        raise NotImplementedError("Subclasses must implement get_import_helper()")

    def get_import_method_name(self):
        raise NotImplementedError("Subclasses must implement get_import_method_name()")

    def get_import_type_name(self):
        raise NotImplementedError("Subclasses must implement get_import_type_name()")

    def get_import_title(self):
        raise NotImplementedError("Subclasses must implement get_import_title()")

    def get_csv_headers(self):
        raise NotImplementedError("Subclasses must implement get_csv_headers()")

    def format_results(self, result, is_wet_run):
        raise NotImplementedError("Subclasses must implement format_results()")

    def import_job_status(self, request, job_id):
        try:
            job = ImportJob.objects.get(id=job_id, user=request.user)

            # Chercher les résultats stocké en memoire
            cached_result = _import_results.get(str(job_id), {})

            response_data = {
                "status": job.status,
                "messages": cached_result.get("messages", []),
                "error_message": cached_result.get("error_message", ""),
            }

            if job.status in ["completed", "failed"] and str(job_id) in _import_results:
                del _import_results[str(job_id)]

            return JsonResponse(response_data)
        except ImportJob.DoesNotExist:
            return JsonResponse({"error": "Job not found"}, status=404)
