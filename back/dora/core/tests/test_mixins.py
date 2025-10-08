import json
from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import StreamingHttpResponse
from django.test import RequestFactory, TestCase
from django.utils.html import format_html
from model_bakery import baker

from dora.core.mixins import BaseImportAdminMixin


class ConcreteImportAdminMixin(BaseImportAdminMixin):
    def __init__(self):
        self.import_helper = Mock()
        self.import_method_name = "import_data"

    def get_import_helper(self):
        return self.import_helper

    def get_import_method_name(self):
        return self.import_method_name

    def format_results(self, result, is_wet_run):
        return []


class BaseImportAdminMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = baker.make("users.User", is_valid=True)

        self.mixin = ConcreteImportAdminMixin()

    def create_csv_file(
        self, content="header1,header2\nvalue1,value2", filename="test.csv", size=None
    ):
        csv_content = content.encode("utf-8")
        if size:
            # Create a file with specific size for testing file size limits
            csv_content = b"a" * size
        return SimpleUploadedFile(filename, csv_content, content_type="text/csv")

    def parse_streaming_response(self, response):
        self.assertIsInstance(response, StreamingHttpResponse)
        messages = []
        for chunk in response.streaming_content:
            line = chunk.decode("utf-8").strip()
            if line:
                messages.append(json.loads(line))
        return messages

    # Tests des erreurs de l'import

    def test_no_csv_file_uploaded(self):
        request = self.factory.post("/import/", {})
        request.user = self.user

        response = self.mixin.import_csv(request)
        messages = self.parse_streaming_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["type"], "error")
        self.assertEqual(messages[0]["error"], "Veuillez sélectionner un fichier CSV.")

    def test_invalid_file_extension(self):
        txt_file = SimpleUploadedFile(
            "test.txt", b"some content", content_type="text/plain"
        )

        request = self.factory.post("/import/", {"csv_file": txt_file})
        request.user = self.user

        response = self.mixin.import_csv(request)
        messages = self.parse_streaming_response(response)

        expected_message = (
            "<b>Échec de l'import - Format de fichier non valide</b><br/>"
            "Le fichier n'est pas au format CSV attendu. Assurez-vous d'utiliser un fichier .csv avec des colonnes séparées par des virgules."
        )
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["type"], "error")
        self.assertEqual(messages[0]["error"], str(format_html(expected_message)))

    def test_file_too_large(self):
        large_file = self.create_csv_file(
            content="header\nvalue",
            size=11 * 1024 * 1024,  # 11MB, exceeds 10MB limit
        )

        request = self.factory.post("/import/", {"csv_file": large_file})
        request.user = self.user

        response = self.mixin.import_csv(request)
        messages = self.parse_streaming_response(response)

        expected_message = (
            "<b>Échec de l'import - Fichier trop volumineux</b><br/>"
            "Le fichier doit faire moins de 10 Mio."
        )
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["type"], "error")
        self.assertEqual(messages[0]["error"], expected_message)

    @patch("dora.core.mixins.io.TextIOWrapper")
    def test_unicode_decode_error(self, mock_wrapper):
        mock_wrapper.side_effect = UnicodeDecodeError(
            "utf-8", b"", 0, 1, "invalid start byte"
        )

        csv_file = self.create_csv_file()

        request = self.factory.post("/import/", {"csv_file": csv_file})
        request.user = self.user

        response = self.mixin.import_csv(request)
        messages = self.parse_streaming_response(response)

        expected_message = (
            "<b>Échec de l'import - Erreur d'encodage du fichier</b><br/>"
            "Le fichier contient des caractères spéciaux illisibles. Sauvegardez votre fichier en UTF-8 et relancez l'import."
        )
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["type"], "error")
        self.assertEqual(messages[0]["error"], str(format_html(expected_message)))

    def test_general_exception_handling(self):
        mock_import_method = Mock(side_effect=ValueError("Unexpected error"))
        self.mixin.import_helper.import_data = mock_import_method

        csv_file = self.create_csv_file()

        request = self.factory.post("/import/", {"csv_file": csv_file})
        request.user = self.user

        response = self.mixin.import_csv(request)
        messages = self.parse_streaming_response(response)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["type"], "error")
        self.assertIn("Unexpected error", messages[0]["error"])

    # Tests des cas de succès de l'import

    def test_successful_import_with_defaults(self):
        csv_file = self.create_csv_file()

        request = self.factory.post("/import/", {"csv_file": csv_file})
        request.user = self.user

        mock_import_method = Mock(return_value={"success": True})
        self.mixin.import_helper.import_data = mock_import_method

        response = self.mixin.import_csv(request)
        self.assertIsInstance(response, StreamingHttpResponse)

        # Consume the streaming response
        list(response.streaming_content)

        mock_import_method.assert_called_once()
        call_args = mock_import_method.call_args

        self.assertEqual(call_args[0][1], request.user)
        self.assertEqual(call_args[0][2]["value"], "test")
        self.assertEqual(call_args[0][2]["label"], "DORA")
        self.assertEqual(call_args[1]["wet_run"], True)
        self.assertEqual(call_args[1]["should_remove_first_two_lines"], False)
        self.assertIn("progress_callback", call_args[1])

    def test_import_with_custom_parameters(self):
        csv_file = self.create_csv_file(filename="custom_file.csv")

        request = self.factory.post(
            "/import/",
            {
                "csv_file": csv_file,
                "test_run": "on",
                "source_label": "Custom Source",
                "should_remove_instructions": "on",
            },
        )
        request.user = self.user

        mock_import_method = Mock(return_value={"success": True})
        self.mixin.import_helper.import_data = mock_import_method

        response = self.mixin.import_csv(request)
        self.assertIsInstance(response, StreamingHttpResponse)

        # Consume the streaming response
        list(response.streaming_content)

        call_args = mock_import_method.call_args

        self.assertEqual(call_args[0][2]["value"], "custom_file")
        self.assertEqual(call_args[0][2]["label"], "Custom Source")
        self.assertEqual(call_args[1]["wet_run"], False)
        self.assertEqual(call_args[1]["should_remove_first_two_lines"], True)

    def test_empty_source_label_uses_default(self):
        csv_file = self.create_csv_file()

        request = self.factory.post(
            "/import/",
            {
                "csv_file": csv_file,
                "source_label": "   ",  # whitespace only
            },
        )
        request.user = self.user

        mock_import_method = Mock(return_value={"success": True})
        self.mixin.import_helper.import_data = mock_import_method

        response = self.mixin.import_csv(request)
        # Consume the streaming response
        list(response.streaming_content)

        call_args = mock_import_method.call_args
        self.assertEqual(call_args[0][2]["label"], "DORA")  # should use default

    def test_source_info_filename_extraction(self):
        test_cases = [
            ("simple.csv", "simple"),
            ("file.with.dots.csv", "file.with.dots"),
            ("file.CSV", "file"),
        ]

        for filename, expected_value in test_cases:
            with self.subTest(filename=filename):
                csv_file = self.create_csv_file(filename=filename)

                request = self.factory.post("/import/", {"csv_file": csv_file})
                request.user = self.user

                mock_import_method = Mock(return_value={"success": True})
                self.mixin.import_helper.import_data = mock_import_method

                response = self.mixin.import_csv(request)
                # Consume the streaming response
                list(response.streaming_content)

                call_args = mock_import_method.call_args
                source_info = call_args[0][2]
                self.assertEqual(source_info["value"], expected_value)

    # Tests des méthodes non-implémentés

    def test_get_import_helper_not_implemented(self):
        base_mixin = BaseImportAdminMixin()

        with self.assertRaises(NotImplementedError) as context:
            base_mixin.get_import_helper()

        self.assertIn(
            "Subclasses must implement get_import_helper()", str(context.exception)
        )

    def test_get_import_method_name_not_implemented(self):
        base_mixin = BaseImportAdminMixin()

        with self.assertRaises(NotImplementedError) as context:
            base_mixin.get_import_method_name()

        self.assertIn(
            "Subclasses must implement get_import_method_name()", str(context.exception)
        )

    def test_handle_import_results_not_implemented(self):
        base_mixin = BaseImportAdminMixin()
        result = Mock()

        with self.assertRaises(NotImplementedError) as context:
            base_mixin.format_results(result, True)

        self.assertIn(
            "Subclasses must implement format_results()", str(context.exception)
        )
