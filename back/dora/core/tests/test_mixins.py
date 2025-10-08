from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
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

    def format_results(self, request, result, is_wet_run):
        return Mock(status_code=200)


@patch("dora.core.mixins.redirect")
@patch("dora.core.mixins.messages")
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

    # Tests des erreurs de l'import

    def test_no_csv_file_uploaded(self, mock_messages, mock_redirect):
        request = self.factory.post("/import/", {})
        request.user = self.user

        self.mixin.import_csv(request)

        mock_messages.error.assert_called_once_with(
            request, "Veuillez sélectionner un fichier CSV."
        )
        mock_redirect.assert_called_once_with(".")

    def test_invalid_file_extension(self, mock_messages, mock_redirect):
        txt_file = SimpleUploadedFile(
            "test.txt", b"some content", content_type="text/plain"
        )

        request = self.factory.post("/import/", {"csv_file": txt_file})
        request.user = self.user

        self.mixin.import_csv(request)

        expected_message = (
            "<b>Échec de l'import - Format de fichier non valide</b><br/>"
            "Le fichier n'est pas au format CSV attendu. Assurez-vous d'utiliser un fichier .csv avec des colonnes séparées par des virgules."
        )
        mock_messages.error.assert_called_once_with(
            request, format_html(expected_message)
        )
        mock_redirect.assert_called_once_with(".")

    def test_file_too_large(self, mock_messages, mock_redirect):
        large_file = self.create_csv_file(
            content="header\nvalue",
            size=11 * 1024 * 1024,  # 11MB, exceeds 10MB limit
        )

        request = self.factory.post("/import/", {"csv_file": large_file})
        request.user = self.user

        self.mixin.import_csv(request)

        expected_message = (
            "<b>Échec de l'import - Fichier trop volumineux</b><br/>"
            "Le fichier doit faire moins de 10 Mio."
        )
        mock_messages.error.assert_called_once_with(request, expected_message)
        mock_redirect.assert_called_once_with(".")

    @patch("dora.core.mixins.io.TextIOWrapper")
    def test_unicode_decode_error(self, mock_wrapper, mock_messages, mock_redirect):
        mock_wrapper.side_effect = UnicodeDecodeError(
            "utf-8", b"", 0, 1, "invalid start byte"
        )

        csv_file = self.create_csv_file()

        request = self.factory.post("/import/", {"csv_file": csv_file})
        request.user = self.user

        self.mixin.import_csv(request)

        expected_message = (
            "<b>Échec de l'import - Erreur d'encodage du fichier</b><br/>"
            "Le fichier contient des caractères spéciaux illisibles. Sauvegardez votre fichier en UTF-8 et relancez l'import."
        )
        mock_messages.error.assert_called_once_with(
            request, format_html(expected_message)
        )
        mock_redirect.assert_called_once_with(".")

    def test_general_exception_handling(self, mock_messages, mock_redirect):
        mock_import_method = Mock(side_effect=ValueError("Unexpected error"))
        self.mixin.import_helper.import_data = mock_import_method

        csv_file = self.create_csv_file()

        request = self.factory.post("/import/", {"csv_file": csv_file})
        request.user = self.user

        self.mixin.import_csv(request)

        mock_messages.error.assert_called_once_with(
            request,
            "<b>Échec de l'import - Erreur inattendue</b><br/>L'erreur suivante s'est produite :<br/>Unexpected error<br/>Si le problème persiste, contactez les développeurs.",
        )
        mock_redirect.assert_called_once_with(".")

    # Tests des cas de succès de l'import

    def test_successful_import_with_defaults(self, mock_messages, mock_redirect):
        csv_file = self.create_csv_file()

        request = self.factory.post("/import/", {"csv_file": csv_file})
        request.user = self.user

        mock_import_method = Mock()
        self.mixin.import_helper.import_data = mock_import_method

        expected_response = Mock(status_code=200)
        with patch.object(
            self.mixin, "handle_import_results", return_value=expected_response
        ):
            result = self.mixin.import_csv(request)

            mock_import_method.assert_called_once()
            call_args = mock_import_method.call_args

            self.assertEqual(call_args[0][1], request.user)
            self.assertEqual(call_args[0][2]["value"], "test")
            self.assertEqual(call_args[0][2]["label"], "DORA")
            self.assertEqual(call_args[1]["wet_run"], True)
            self.assertEqual(call_args[1]["should_remove_first_two_lines"], False)

            self.assertEqual(result, expected_response)

    def test_import_with_custom_parameters(self, mock_messages, mock_redirect):
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

        mock_import_method = Mock()
        self.mixin.import_helper.import_data = mock_import_method

        expected_response = Mock(status_code=200)
        with patch.object(
            self.mixin, "handle_import_results", return_value=expected_response
        ):
            self.mixin.import_csv(request)

            call_args = mock_import_method.call_args

            self.assertEqual(call_args[0][2]["value"], "custom_file")
            self.assertEqual(call_args[0][2]["label"], "Custom Source")
            self.assertEqual(call_args[1]["wet_run"], False)
            self.assertEqual(call_args[1]["should_remove_first_two_lines"], True)

    def test_empty_source_label_uses_default(self, mock_messages, mock_redirect):
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

        with patch.object(self.mixin, "handle_import_results", return_value=Mock()):
            self.mixin.import_csv(request)

            call_args = mock_import_method.call_args
            self.assertEqual(call_args[0][2]["label"], "DORA")  # should use default

    def test_source_info_filename_extraction(self, mock_messages, mock_redirect):
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

                mock_import_method = Mock()
                self.mixin.import_helper.import_data = mock_import_method

                with patch.object(
                    self.mixin, "handle_import_results", return_value=Mock()
                ):
                    self.mixin.import_csv(request)

                    call_args = mock_import_method.call_args
                    source_info = call_args[0][2]
                    self.assertEqual(source_info["value"], expected_value)

    # Tests des méthodes non-implémentés

    def test_get_import_helper_not_implemented(self, mock_messages, mock_redirect):
        base_mixin = BaseImportAdminMixin()

        with self.assertRaises(NotImplementedError) as context:
            base_mixin.get_import_helper()

        self.assertIn(
            "Subclasses must implement get_import_helper()", str(context.exception)
        )

    def test_get_import_method_name_not_implemented(self, mock_messages, mock_redirect):
        base_mixin = BaseImportAdminMixin()

        with self.assertRaises(NotImplementedError) as context:
            base_mixin.get_import_method_name()

        self.assertIn(
            "Subclasses must implement get_import_method_name()", str(context.exception)
        )

    def test_handle_import_results_not_implemented(self, mock_messages, mock_redirect):
        base_mixin = BaseImportAdminMixin()
        request = Mock()
        result = Mock()

        with self.assertRaises(NotImplementedError) as context:
            base_mixin.format_results(request, result, True)

        self.assertIn(
            "Subclasses must implement _handle_import_results()", str(context.exception)
        )
