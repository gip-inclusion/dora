import pytest

from dora.core.test_utils import make_user
from dora.oidc.models import UserSession


@pytest.fixture
def user():
    return make_user()


def test_create_user_session(client, user):
    client.force_login(user)

    user_sessions = UserSession.objects.filter(user=user)

    assert len(user_sessions) == 1, "Une seule session possible pour cet utilisateur"

    [user_session] = user_sessions
    assert user_session.user == user, "Utilisateur de la session incorrect"


def test_delete_user_session(client, user):
    client.force_login(user)

    # 1 - destruction de la session
    user_sessions_before_session_delete = UserSession.objects.filter(user=user)
    assert user_sessions_before_session_delete.count() == 1, (
        "La session doit exister avant suppression"
    )
    user_session = user_sessions_before_session_delete.first()
    user_session.session.delete()
    user_sessions_after_session_delete = UserSession.objects.filter(user=user)

    assert user_sessions_after_session_delete.count() == 0, (
        "Session supprimée : les informations de session devraient avoir été détruites"
    )

    # 2 - destruction de l'utilisateur
    client.force_login(user)
    user_sessions_before_user_delete = UserSession.objects.filter(user=user)
    assert user_sessions_before_user_delete.count() == 1, (
        "La session doit exister avant suppression de l'utilisateur"
    )

    # Stocker la PK avant la suppression
    user_pk = user.pk
    user.delete()
    user_sessions_after_user_delete = UserSession.objects.filter(user_id=user_pk)

    assert user_sessions_after_user_delete.count() == 0, (
        "Utilisateur supprimé : les informations de session devraient avoir été détruites"
    )
