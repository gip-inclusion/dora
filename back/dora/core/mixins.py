import csv
import io

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.html import format_html


class BaseImportAdminMixin:
    upload_size_limit_in_bytes = 10 * 1024 * 1024  # 10MB
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
                "<b>Échec de l'import - Fichier trop volumineux</b><br/>Le fichier doit faire moins de 10 Mio.",
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
            source_info = {
                "value": csv_file.name.rsplit(".", 1)[0],
                "label": source_label or self.default_source_label,
            }
            reader = csv.reader(io.TextIOWrapper(csv_file, encoding="utf-8"))

            helper = self.get_import_helper()
            method_name = self.get_import_method_name()
            import_method = getattr(helper, method_name)

            result = import_method(
                reader,
                request.user,
                source_info,
                wet_run=is_wet_run,
                should_remove_first_two_lines=should_remove_instructions_from_csv,
            )
            return self.handle_import_results(request, result, is_wet_run)
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

    def get_import_helper(self):
        """Override this method to return the appropriate import helper."""
        raise NotImplementedError("Subclasses must implement get_import_helper()")

    def get_import_method_name(self):
        """Override this method to return the import method name."""
        raise NotImplementedError("Subclasses must implement get_import_method_name()")

    def handle_import_results(self, request, result, is_wet_run):
        raise NotImplementedError("Subclasses must implement _handle_import_results()")
