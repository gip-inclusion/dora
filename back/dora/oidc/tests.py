import time
import uuid

import jwt
import pytest
from django.conf import settings
from django.core.cache import cache
from django.db.utils import IntegrityError
from requests_mock import Mocker

from dora.core.test_utils import make_structure, make_user
from dora.structures.models import StructurePutativeMember
from dora.users.models import User

from . import OIDCError
from .utils import updated_ic_user


@pytest.fixture
def client_with_cache(client):
    cache.set(
        "oidc-state-foo",
        {
            "state": "foo",
            "nonce": "bar",
            "redirect_uri": "/",
        },
    )
    return client


def make_ic_token(**kwargs):
    token = jwt.encode(
        payload={
            "iss": settings.IC_ISSUER_ID,
            "aud": [settings.IC_CLIENT_ID],
            "exp": time.time() + 10000,
            "nonce": "bar",
            **kwargs,
        },
        key="foo_key",
    )
    return token


def test_updated_ic_user():
    invited_user = make_user()
    invitation = StructurePutativeMember(user=invited_user, structure=make_structure())
    invitation.save()
    invited_user.putative_membership.add(invitation)

    ic_user = make_user(ic_id=uuid.uuid4())

    # cas "normal" : aucun changement de l'email de d'utilisateur
    user, should_update = updated_ic_user(ic_user, ic_user.email)
    assert not should_update
    assert user.email == ic_user.email

    # cas à gérer : changement de l'email de l'utilisateur IC par un email d'utilisateur invité
    user, should_update = updated_ic_user(ic_user, invited_user.email)
    assert should_update
    assert user.email == invited_user.email

    # migration des invitations
    invitation.refresh_from_db()
    assert invitation.user == ic_user

    # l'ancien utilisateur n'existe plus
    with pytest.raises(User.DoesNotExist):
        invited_user.refresh_from_db()


def test_updated_user_member_of_structure(client_with_cache, settings):
    member_user = make_user(structure=make_structure())
    ic_user = make_user(ic_id=uuid.uuid4())

    # doit retourner une erreur si on essaye de modifier un utilisateur membre d'une structure
    with pytest.raises(OIDCError):
        _, _ = updated_ic_user(ic_user, member_user.email)


def test_login_ic_user_with_updated_email(client_with_cache, settings, requests_mock):
    # création d'un utilisateur DORA, par ex. suite à une invitation
    invited_user = make_user()
    # création un utilisateur déjà connecté à IC
    ic_user = make_user(ic_id=uuid.uuid4())

    with Mocker() as m:
        # connexion IC avec un e-mail mis à jour :
        token = make_ic_token(
            sub=str(ic_user.ic_id),
            email=invited_user.email,
            given_name=invited_user.first_name,
            family_name=invited_user.last_name,
        )
        # on détourne l'URL d'obtention du token IC
        m.post(settings.IC_TOKEN_URL, json={"id_token": token})

        try:
            response = client_with_cache.post(
                "/inclusion-connect-authenticate/",
                data={
                    "code": "anycode",
                    "state": "foo",
                    "frontend_state": "foo",
                },
            )

            assert 200 == response.status_code
        except IntegrityError:
            # le cas d'erreur à traiter
            pytest.fail(
                "Problème d'intégrité de l'e-mail IC mis à jour toujours présent"
            )
