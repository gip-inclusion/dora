from dateutil.relativedelta import relativedelta
from django.utils import timezone
from freezegun import freeze_time

from ..models import ORIENTATION_QUERY_LINK_TTL_DAY


def test_query_expires_at(orientation):
    assert not orientation.query_expired

    # pas de refresh si pas expiré
    h = orientation.get_query_id_hash()
    orientation.refresh_query_expiration_date()
    assert h == orientation.get_query_id_hash()

    with freeze_time(
        time_to_freeze=timezone.now()
        + relativedelta(days=ORIENTATION_QUERY_LINK_TTL_DAY)
    ):
        assert orientation.query_expired


def test_hash_update(orientation):
    h = orientation.get_query_id_hash()
    orientation.query_expires_at = timezone.now()

    assert h != orientation.get_query_id_hash()
