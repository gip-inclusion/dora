import csv
import io
import json
import sys

from django.contrib import messages
from django.http import StreamingHttpResponse
from django.shortcuts import redirect
from django.utils.html import format_html


class BaseImportAdminMixin:
    upload_size_limit_in_bytes = 10 * 1024 * 1024  # 10MB
    default_source_label = "DORA"

    def import_csv(self, request):
        # Check if this is a streaming request (AJAX)
        is_streaming = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            if is_streaming:
                return StreamingHttpResponse(
                    [json.dumps({"type": "error", "error": "Veuillez sélectionner un fichier CSV."}) + "\n"],
                    content_type="application/json"
                )
            messages.error(request, "Veuillez sélectionner un fichier CSV.")
            return redirect(".")

        if not csv_file.name.lower().endswith(".csv"):
            error_msg = format_html(
                "<b>Échec de l'import - Format de fichier non valide</b><br/>"
                "Le fichier n'est pas au format CSV attendu. Assurez-vous d'utiliser un fichier .csv avec des colonnes séparées par des virgules.",
            )
            if is_streaming:
                return StreamingHttpResponse(
                    [json.dumps({"type": "error", "error": str(error_msg)}) + "\n"],
                    content_type="application/json"
                )
            messages.error(request, error_msg)
            return redirect(".")

        if csv_file.size > self.upload_size_limit_in_bytes:
            error_msg = "<b>Échec de l'import - Fichier trop volumineux</b><br/>Le fichier doit faire moins de 10 Mio."
            if is_streaming:
                return StreamingHttpResponse(
                    [json.dumps({"type": "error", "error": error_msg}) + "\n"],
                    content_type="application/json"
                )
            messages.error(request, error_msg)
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

            # If streaming, return StreamingHttpResponse
            if is_streaming:
                return StreamingHttpResponse(
                    self._streaming_import_generator(
                        import_method,
                        reader,
                        request.user,
                        source_info,
                        is_wet_run,
                        should_remove_instructions_from_csv
                    ),
                    content_type="application/json"
                )

            # Otherwise, use the normal flow
            result = import_method(
                reader,
                request.user,
                source_info,
                wet_run=is_wet_run,
                should_remove_first_two_lines=should_remove_instructions_from_csv,
            )

            # Handle results and display messages
            self.handle_import_results(request, result, is_wet_run)
            return redirect(".")

        except UnicodeDecodeError:
            error_msg = format_html(
                "<b>Échec de l'import - Erreur d'encodage du fichier</b><br/>"
                "Le fichier contient des caractères spéciaux illisibles. Sauvegardez votre fichier en UTF-8 et relancez l'import.",
            )
            if is_streaming:
                return StreamingHttpResponse(
                    [json.dumps({"type": "error", "error": str(error_msg)}) + "\n"],
                    content_type="application/json"
                )
            messages.error(request, error_msg)
            return redirect(".")
        except Exception as e:
            error_msg = format_html(
                "<b>Échec de l'import - Erreur inattendue</b><br/>"
                "L'erreur suivante s'est produite :<br/>"
                f"{e}<br/>"
                "Si le problème persiste, contactez les développeurs.",
            )
            if is_streaming:
                return StreamingHttpResponse(
                    [json.dumps({"type": "error", "error": str(error_msg)}) + "\n"],
                    content_type="application/json"
                )
            messages.error(request, error_msg)
            return redirect(".")

    def get_import_helper(self):
        """Override this method to return the appropriate import helper."""
        raise NotImplementedError("Subclasses must implement get_import_helper()")

    def get_import_method_name(self):
        """Override this method to return the import method name."""
        raise NotImplementedError("Subclasses must implement get_import_method_name()")

    def handle_import_results(self, request, result, is_wet_run):
        raise NotImplementedError("Subclasses must implement _handle_import_results()")

    def _streaming_import_generator(
        self, import_method, reader, user, source_info, is_wet_run, should_remove_instructions
    ):
        """Generator that yields progress updates and final result as JSON."""

        class StreamCapture:
            """Custom file-like object that captures lines."""
            def __init__(self, generator_callback):
                self.generator_callback = generator_callback
                self._buffer = ""

            def write(self, text):
                self._buffer += text
                # Yield complete lines
                while "\n" in self._buffer:
                    idx = self._buffer.index("\n")
                    line = self._buffer[:idx]
                    self._buffer = self._buffer[idx + 1:]
                    if line.strip():
                        self.generator_callback(line)
                return len(text)

            def flush(self):
                pass

        def yield_json(data):
            yield json.dumps(data) + "\n"

        output_lines = []

        def capture_line(captured_line):
            output_lines.append(captured_line)

        # Capture stdout
        stream_capture = StreamCapture(capture_line)
        old_stdout = sys.stdout
        sys.stdout = stream_capture

        try:
            # Run the import
            result = import_method(
                reader,
                user,
                source_info,
                wet_run=is_wet_run,
                should_remove_first_two_lines=should_remove_instructions,
            )

            # Yield all captured lines as progress
            for captured_line in output_lines:
                yield from yield_json({"type": "progress", "message": captured_line})

            # Collect messages by creating a mock request with message storage
            from django.contrib.messages.storage.base import BaseStorage

            class MessageCollector(BaseStorage):
                def __init__(self):
                    self._queued_messages = []
                    self.used = False
                    self.added_new = False

                def _store(self, messages_list, response, *args, **kwargs):
                    pass

                def _get(self, *args, **kwargs):
                    return [], False

            # Create a mock request with proper message storage
            mock_request = type('MockRequest', (), {
                '_messages': MessageCollector(),
                'session': {},
                'COOKIES': {},
                'META': {}
            })()

            # Call handle_import_results to collect messages
            self.handle_import_results(mock_request, result, is_wet_run)

            # Extract messages
            final_messages = []
            for msg in mock_request._messages._queued_messages:
                final_messages.append({
                    "level": msg.level_tag,
                    "message": str(msg.message)
                })

            # Yield final result with messages
            yield from yield_json({
                "type": "complete",
                "result": result,
                "messages": final_messages
            })

        except Exception as e:
            # Yield error
            yield from yield_json({
                "type": "error",
                "error": str(e)
            })
        finally:
            sys.stdout = old_stdout
