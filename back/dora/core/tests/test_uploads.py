from unittest.mock import patch

from django.utils import timezone

from dora.core.uploads import iter_managed_objects


@patch("dora.core.uploads.default_storage")
def test_iter_managed_objects_skips_unmanaged_path(mock_storage, caplog):
    now = timezone.now()
    mock_page = {
        "Contents": [
            {"Key": "local/#orientations/abc/file.pdf", "LastModified": now},
            {"Key": "local/some-other-prefix/file.pdf", "LastModified": now},
        ]
    }
    mock_storage.connection.meta.client.get_paginator.return_value.paginate.return_value = [
        mock_page
    ]

    keys = [key for key, _ in iter_managed_objects()]

    assert "local/#orientations/abc/file.pdf" in keys
    assert "local/some-other-prefix/file.pdf" not in keys
    assert "1 fichier(s) inattendu(s) dans le bucket S3" in [
        record.getMessage() for record in caplog.records
    ]
