import csv
import io
import json

from django.http import StreamingHttpResponse
from django.utils.html import format_html


class BaseImportAdminMixin:
    upload_size_limit_in_bytes = 10 * 1024 * 1024  # 10MB
    default_source_label = "DORA"

    def import_csv(self, request):
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            error_msg = "Veuillez sélectionner un fichier CSV."
            return StreamingHttpResponse(
                [json.dumps({"type": "error", "error": error_msg}) + "\n"],
                content_type="application/json",
            )

        if not csv_file.name.lower().endswith(".csv"):
            error_msg = format_html(
                "<b>Échec de l'import - Format de fichier non valide</b><br/>"
                "Le fichier n'est pas au format CSV attendu. Assurez-vous d'utiliser un fichier .csv avec des colonnes séparées par des virgules.",
            )

            return StreamingHttpResponse(
                [json.dumps({"type": "error", "error": str(error_msg)}) + "\n"],
                content_type="application/json",
            )

        if csv_file.size > self.upload_size_limit_in_bytes:
            error_msg = "<b>Échec de l'import - Fichier trop volumineux</b><br/>Le fichier doit faire moins de 10 Mio."
            return StreamingHttpResponse(
                [json.dumps({"type": "error", "error": error_msg}) + "\n"],
                content_type="application/json",
            )

        try:
            is_wet_run = request.POST.get("test_run") != "on"
            source_label = request.POST.get(
                "source_label", self.default_source_label
            ).strip()
            should_remove_instructions_from_csv = (
                request.POST.get("should_remove_instructions") == "on"
            )
            source_info = {
                "value": csv_file.name.rsplit(".", 1)[0],
                "label": source_label or self.default_source_label,
            }
            reader = csv.reader(io.TextIOWrapper(csv_file, encoding="utf-8"))

            helper = self.get_import_helper()
            method_name = self.get_import_method_name()
            import_method = getattr(helper, method_name)

            return StreamingHttpResponse(
                self._streaming_import_generator(
                    import_method,
                    reader,
                    request.user,
                    source_info,
                    is_wet_run,
                    should_remove_instructions_from_csv,
                ),
                content_type="application/json",
            )

        except UnicodeDecodeError:
            error_msg = format_html(
                "<b>Échec de l'import - Erreur d'encodage du fichier</b><br/>"
                "Le fichier contient des caractères spéciaux illisibles. Sauvegardez votre fichier en UTF-8 et relancez l'import.",
            )
            return StreamingHttpResponse(
                [json.dumps({"type": "error", "error": str(error_msg)}) + "\n"],
                content_type="application/json",
            )
        except Exception as e:
            error_msg = format_html(
                "<b>Échec de l'import - Erreur inattendue</b><br/>"
                "L'erreur suivante s'est produite :<br/>"
                f"{e}<br/>"
                "Si le problème persiste, contactez les développeurs.",
            )
            return StreamingHttpResponse(
                [json.dumps({"type": "error", "error": str(error_msg)}) + "\n"],
                content_type="application/json",
            )

    def get_import_helper(self):
        raise NotImplementedError("Subclasses must implement get_import_helper()")

    def get_import_method_name(self):
        raise NotImplementedError("Subclasses must implement get_import_method_name()")

    def format_results(self, result, is_wet_run):
        raise NotImplementedError("Subclasses must implement format_results()")

    def _streaming_import_generator(
        self,
        import_method,
        reader,
        user,
        source_info,
        is_wet_run,
        should_remove_instructions,
    ):
        """Generator that yields progress updates and final result as JSON."""

        def yield_json(data):
            yield json.dumps(data) + "\n"

        try:
            result = import_method(
                reader,
                user,
                source_info,
                wet_run=is_wet_run,
                should_remove_first_two_lines=should_remove_instructions,
            )

            messages = self.format_results(result, is_wet_run)

            yield from yield_json(
                {"type": "complete", "result": result, "messages": messages}
            )

        except Exception as e:
            yield from yield_json({"type": "error", "error": str(e)})
