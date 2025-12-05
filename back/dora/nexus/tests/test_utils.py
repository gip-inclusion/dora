import datetime

import pytest
from freezegun import freeze_time
from jwcrypto import jwt

from dora.core.test_utils import make_user
from dora.nexus.utils import EXPIRY_DELAY_SECONDS, decode_jwt, generate_jwt


@pytest.fixture
def user():
    return make_user()


def test_generate_and_decode_jwt(user):
    with freeze_time() as frozen_now:
        token = generate_jwt(user)

        # generated token requires a key to decode
        with pytest.raises(KeyError):
            jwt.JWT(jwt=token).claims

        # It contains the user email
        assert decode_jwt(token) == {"email": user.email}

        # Wait for the JWT to expire, and then extra time for the leeway.
        leeway = 60
        frozen_now.tick(datetime.timedelta(seconds=EXPIRY_DELAY_SECONDS + leeway + 1))
        with pytest.raises(ValueError):
            decode_jwt(token)
