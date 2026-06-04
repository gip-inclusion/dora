from datetime import timedelta
from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.utils import timezone

from dora.core.test_utils import make_orientation, make_service

BUCKET_OBJECTS = "dora.core.management.commands.delete_orphaned_uploads._iter_objects"
STORAGE_DELETE = (
    "dora.core.management.commands.delete_orphaned_uploads.default_storage.delete"
)


def s3_object(key, age_hours=10):
    return (key, timezone.now() - timedelta(hours=age_hours))


def call_cmd(**kwargs):
    call_command("delete_orphaned_uploads", stdout=StringIO(), **kwargs)


@pytest.mark.django_db
@patch(STORAGE_DELETE)
@patch(BUCKET_OBJECTS)
def test_dry_run_does_not_delete(mock_iter, mock_delete):
    mock_iter.return_value = [s3_object("orphan.pdf")]

    call_cmd()

    mock_delete.assert_not_called()


@pytest.mark.django_db
@patch(STORAGE_DELETE)
@patch(BUCKET_OBJECTS)
def test_wet_run_deletes_orphan(mock_iter, mock_delete):
    mock_iter.return_value = [s3_object("orphan.pdf")]

    call_cmd(wet_run=True)

    mock_delete.assert_called_once_with("orphan.pdf")


@pytest.mark.django_db
@patch(STORAGE_DELETE)
@patch(BUCKET_OBJECTS)
def test_skips_orientation_attachment(mock_iter, mock_delete):
    make_orientation(beneficiary_attachments=["referenced.pdf"])
    mock_iter.return_value = [s3_object("referenced.pdf")]

    call_cmd(wet_run=True)

    mock_delete.assert_not_called()


@pytest.mark.django_db
@patch(STORAGE_DELETE)
@patch(BUCKET_OBJECTS)
def test_skips_service_form(mock_iter, mock_delete):
    make_service(forms=["referenced_form.pdf"])
    mock_iter.return_value = [s3_object("referenced_form.pdf")]

    call_cmd(wet_run=True)

    mock_delete.assert_not_called()


@pytest.mark.django_db
@patch(STORAGE_DELETE)
@patch(BUCKET_OBJECTS)
def test_skips_recent_file(mock_iter, mock_delete):
    mock_iter.return_value = [s3_object("recent.pdf", age_hours=1)]

    call_cmd(wet_run=True)

    mock_delete.assert_not_called()


@pytest.mark.django_db
@patch(STORAGE_DELETE)
@patch(BUCKET_OBJECTS)
def test_deletes_only_old_orphans(mock_iter, mock_delete):
    make_orientation(beneficiary_attachments=["referenced.pdf"])
    mock_iter.return_value = [
        s3_object("referenced.pdf", age_hours=10),
        s3_object("recent_orphan.pdf", age_hours=1),
        s3_object("old_orphan.pdf", age_hours=10),
    ]

    call_cmd(wet_run=True)

    mock_delete.assert_called_once_with("old_orphan.pdf")
