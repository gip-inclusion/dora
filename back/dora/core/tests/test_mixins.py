from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase
from model_bakery import baker

from dora.core.mixins import BaseImportAdminMixin
from dora.core.models import ImportJob


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

    def get_import_type_name(self):
        return "services"

    def get_import_title(self):
        return "Import services"

    def get_csv_headers(self):
        return ["header1", "header2"]

    def _create_failed_job(self, request, filename, message):
        return {}


class BaseImportAdminMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = baker.make("users.User", is_valid=True)

        self.mixin = ConcreteImportAdminMixin()

        self.thread_mock = Mock()

        def run_sync(target=None, args=None, **kwargs):
            # Le threading doit être synchrone pour les tests
            self.thread_mock.start = lambda: target(*args)
            return self.thread_mock

        self.run_sync = run_sync

    def create_csv_file(
        self, content="header1,header2\nvalue1,value2", filename="test.csv", size=None
    ):
        csv_content = content.encode("utf-8")
        if size:
            # Créer un fichier avec une taille spécifique
            csv_content = b"a" * size
        return SimpleUploadedFile(filename, csv_content, content_type="text/csv")

    # Tests des erreurs de l'import

    def test_no_csv_file_uploaded(self):
        request = self.factory.post("/import/", {})
        request.user = self.user

        with patch.object(self.mixin, "_create_failed_job") as mock_failed:
            mock_failed.return_value = Mock()
            self.mixin.import_csv(request)

            mock_failed.assert_called_once()
            call_args = mock_failed.call_args[0]
            self.assertEqual(call_args[1], "fichier-manquant.csv")
            self.assertEqual("Veuillez sélectionner un fichier CSV.", call_args[2])

    def test_invalid_file_extension(self):
        txt_file = SimpleUploadedFile(
            "test.txt", b"some content", content_type="text/plain"
        )

        request = self.factory.post("/import/", {"csv_file": txt_file})
        request.user = self.user

        with patch.object(self.mixin, "_create_failed_job") as mock_failed:
            mock_failed.return_value = Mock()
            self.mixin.import_csv(request)

            mock_failed.assert_called_once()
            call_args = mock_failed.call_args[0]
            self.assertEqual(call_args[1], "test.txt")
            self.assertIn("Format de fichier non valide", call_args[2])

    def test_file_too_large(self):
        large_file = self.create_csv_file(
            content="header\nvalue",
            size=51 * 1024 * 1024,  # 51MB, exceeds 50MB limit
        )

        request = self.factory.post("/import/", {"csv_file": large_file})
        request.user = self.user

        with patch.object(self.mixin, "_create_failed_job") as mock_failed:
            mock_failed.return_value = Mock()
            self.mixin.import_csv(request)

            mock_failed.assert_called_once()
            call_args = mock_failed.call_args[0]
            self.assertIn("Fichier trop volumineux", call_args[2])

    def test_unicode_decode_error(self):
        invalid_file = SimpleUploadedFile(
            "test.csv", b"\xff\xfe", content_type="text/csv"
        )

        request = self.factory.post("/import/", {"csv_file": invalid_file})
        request.user = self.user

        with patch.object(self.mixin, "_create_failed_job") as mock_failed:
            mock_failed.return_value = Mock()
            self.mixin.import_csv(request)

            mock_failed.assert_called_once()
            call_args = mock_failed.call_args[0]
            self.assertIn("Erreur d'encodage", call_args[2])

    @patch("dora.core.mixins.threading.Thread")
    def test_general_exception_handling(self, mock_thread):
        mock_thread.side_effect = self.run_sync

        mock_import_method = Mock(side_effect=ValueError("Unexpected error"))
        self.mixin.import_helper.import_data = mock_import_method

        csv_file = self.create_csv_file()

        request = self.factory.post("/import/", {"csv_file": csv_file})
        request.user = self.user

        with patch("dora.core.mixins.render") as mock_render:
            mock_render.return_value = Mock()
            self.mixin.import_csv(request)

            job = ImportJob.objects.get(user=self.user)
            self.assertEqual(job.status, "failed")

    # Tests des cas de succès de l'import

    @patch("dora.core.mixins.render")
    @patch("dora.core.mixins.threading.Thread")
    def test_successful_import_with_defaults(self, mock_thread, mock_render):
        mock_thread.side_effect = self.run_sync
        mock_render.return_value = Mock(status_code=200)

        csv_file = self.create_csv_file()

        request = self.factory.post("/import/", {"csv_file": csv_file})
        request.user = self.user

        mock_import_method = Mock(return_value={"created_count": 3})
        self.mixin.import_helper.import_data = mock_import_method

        self.mixin.import_csv(request)

        job = ImportJob.objects.get(user=self.user)
        self.assertEqual(job.status, "completed")

        mock_import_method.assert_called_once()
        call_args = mock_import_method.call_args

        self.assertEqual(call_args[0][1], request.user)
        self.assertEqual(call_args[0][2]["value"], "test")
        self.assertEqual(call_args[0][2]["label"], "DORA")
        self.assertEqual(call_args[1]["wet_run"], True)
        self.assertEqual(call_args[1]["should_remove_first_two_lines"], False)

    @patch("dora.core.mixins.render")
    @patch("dora.core.mixins.threading.Thread")
    def test_import_with_custom_parameters(self, mock_thread, mock_render):
        mock_thread.side_effect = self.run_sync
        mock_render.return_value = Mock(status_code=200)

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

        mock_import_method = Mock(return_value={"created_count": 5})
        self.mixin.import_helper.import_data = mock_import_method

        self.mixin.import_csv(request)

        job = ImportJob.objects.get(user=self.user)
        self.assertEqual(job.import_type, "services")
        self.assertEqual(job.filename, "custom_file.csv")
        self.assertEqual(job.status, "completed")

        call_args = mock_import_method.call_args
        self.assertEqual(call_args[0][2]["value"], "custom_file")
        self.assertEqual(call_args[0][2]["label"], "Custom Source")
        self.assertEqual(call_args[1]["wet_run"], False)
        self.assertEqual(call_args[1]["should_remove_first_two_lines"], True)

        mock_render.assert_called_once()
        render_call_args = mock_render.call_args
        context = render_call_args[0][2]
        self.assertEqual(context["filename"], "custom_file.csv")
        self.assertEqual(context["job_id"], str(job.id))

    @patch("dora.core.mixins.render")
    @patch("dora.core.mixins.threading.Thread")
    def test_empty_source_label_uses_default(self, mock_thread, mock_render):
        mock_thread.side_effect = self.run_sync
        mock_render.return_value = Mock()

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

        self.mixin.import_csv(request)

        call_args = mock_import_method.call_args
        self.assertEqual(call_args[0][2]["label"], "DORA")  # should use default

    @patch("dora.core.mixins.render")
    @patch("dora.core.mixins.threading.Thread")
    def test_source_info_filename_extraction(self, mock_thread, mock_render):
        mock_thread.side_effect = self.run_sync
        mock_render.return_value = Mock()

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

                mock_import_method = Mock(return_value={})
                self.mixin.import_helper.import_data = mock_import_method

                self.mixin.import_csv(request)

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

    def test_format_results_not_implemented(self):
        base_mixin = BaseImportAdminMixin()
        result = Mock()

        with self.assertRaises(NotImplementedError) as context:
            base_mixin.format_results(result, True)

        self.assertIn(
            "Subclasses must implement format_results()", str(context.exception)
        )
