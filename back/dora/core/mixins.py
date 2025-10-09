import csv
import io
import threading
import traceback

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.html import format_html

from .models import ImportJob


def sanitize_for_json(obj):
    """Convert non-JSON-serializable objects to serializable ones."""
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize_for_json(item) for item in obj]
    return obj


class BaseImportAdminMixin:
    upload_size_limit_in_bytes = 50 * 1024 * 1024  # 50MB to handle larger CSVs
    default_source_label = "DORA"

    def import_csv(self, request):
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            messages.error(request, "Veuillez sélectionner un fichier CSV.")
            return redirect(".")
        if not csv_file.name.lower().endswith(".csv"):
            messages.error(
                request,
                format_html(
                    "<b>Échec de l'import - Format de fichier non valide</b><br/>"
                    "Le fichier n'est pas au format CSV attendu. Assurez-vous d'utiliser un fichier .csv avec des colonnes séparées par des virgules.",
                ),
            )
            return redirect(".")
        if csv_file.size > self.upload_size_limit_in_bytes:
            messages.error(
                request,
                "<b>Échec de l'import - Fichier trop volumineux</b><br/>Le fichier doit faire moins de 50 Mio.",
            )
            return redirect(".")

        try:
            is_wet_run = request.POST.get("test_run") != "on"
            source_label = request.POST.get(
                "source_label", self.default_source_label
            ).strip()
            should_remove_instructions_from_csv = (
                request.POST.get("should_remove_instructions") == "on"
            )

            # Read CSV content into memory
            csv_content = csv_file.read().decode("utf-8")

            # Count total rows for progress tracking
            total_rows = len(csv_content.splitlines()) - 1  # Exclude header
            if should_remove_instructions_from_csv:
                total_rows = max(0, total_rows - 2)  # Exclude instruction rows

            # Create ImportJob
            import_job = ImportJob.objects.create(
                user=request.user,
                import_type=self.get_import_type_name(),
                filename=csv_file.name,
                status="pending",
                total_rows=total_rows,
            )

            # Prepare import parameters
            source_info = {
                "value": csv_file.name.rsplit(".", 1)[0],
                "label": source_label or self.default_source_label,
            }

            # Start background thread
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

            # Return to form page with job_id to trigger polling
            return render(
                request,
                "admin/import_csv_form.html",
                {
                    "job_id": str(import_job.id),
                    "filename": csv_file.name,
                    "opts": self.model._meta,
                    "title": self.get_import_title(),
                    "csv_headers": self.get_csv_headers(),
                    "has_view_permission": True,
                },
            )

        except UnicodeDecodeError:
            messages.error(
                request,
                format_html(
                    "<b>Échec de l'import - Erreur d'encodage du fichier</b><br/>"
                    "Le fichier contient des caractères spéciaux illisibles. Sauvegardez votre fichier en UTF-8 et relancez l'import.",
                ),
            )
            return redirect(".")
        except Exception as e:
            messages.error(
                request,
                format_html(
                    "<b>Échec de l'import - Erreur inattendue</b><br/>"
                    "L'erreur suivante s'est produite :<br/>"
                    f"{e}<br/>"
                    "Si le problème persiste, contactez les développeurs.",
                ),
            )
            return redirect(".")

    def _run_import_in_background(
        self,
        job_id,
        csv_content,
        user_id,
        source_info,
        is_wet_run,
        should_remove_instructions,
    ):
        """Run import in background thread and update ImportJob status."""
        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            job = ImportJob.objects.get(id=job_id)
            job.status = "processing"
            job.started_at = timezone.now()
            job.save()

            # Get user object
            user = User.objects.get(id=user_id)

            # Create CSV reader from content
            reader = csv.reader(io.StringIO(csv_content))

            # Get import method
            helper = self.get_import_helper()
            method_name = self.get_import_method_name()
            import_method = getattr(helper, method_name)

            # Run import
            result = import_method(
                reader,
                user,
                source_info,
                wet_run=is_wet_run,
                should_remove_first_two_lines=should_remove_instructions,
                import_job=job,  # Pass job for progress updates
            )

            # Update job with results
            job.status = "completed"
            job.completed_at = timezone.now()
            job.result_data = sanitize_for_json(result)
            job.messages = self.format_results(result, is_wet_run)
            job.save()

        except Exception as e:
            # Handle errors
            job = ImportJob.objects.get(id=job_id)
            job.status = "failed"
            job.completed_at = timezone.now()
            job.error_message = f"{str(e)}\n\n{traceback.format_exc()}"
            job.save()

    def get_import_helper(self):
        """Override this method to return the appropriate import helper."""
        raise NotImplementedError("Subclasses must implement get_import_helper()")

    def get_import_method_name(self):
        """Override this method to return the import method name."""
        raise NotImplementedError("Subclasses must implement get_import_method_name()")

    def get_import_type_name(self):
        """Override this method to return a readable import type name."""
        raise NotImplementedError("Subclasses must implement get_import_type_name()")

    def get_import_title(self):
        """Override this method to return the import page title."""
        raise NotImplementedError("Subclasses must implement get_import_title()")

    def get_csv_headers(self):
        """Override this method to return CSV headers for display."""
        raise NotImplementedError("Subclasses must implement get_csv_headers()")

    def format_results(self, result, is_wet_run):
        raise NotImplementedError("Subclasses must implement format_results()")

    def import_job_status(self, request, job_id):
        """API endpoint to check import job status."""
        try:
            job = ImportJob.objects.get(id=job_id, user=request.user)
            return JsonResponse(
                {
                    "status": job.status,
                    "progress": job.progress_percentage,
                    "current_row": job.current_row,
                    "total_rows": job.total_rows,
                    "messages": job.messages,
                    "error_message": job.error_message,
                    "result_data": job.result_data,
                }
            )
        except ImportJob.DoesNotExist:
            return JsonResponse({"error": "Job not found"}, status=404)
