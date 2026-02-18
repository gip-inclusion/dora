import sesame.utils
from django.conf import settings
from django.urls import reverse
from rest_framework.authtoken.models import Token

from dora.core.test_utils import make_user

# note : utilisation de `client` et pas `api_client`

# note : inutile de tester la durée de validité et l'usage unique,
# c'est de la response de `django-sesame`


def test_send_link(client):
    user_ic = make_user(is_active=True)

    response = client.post(
        reverse("send_link"),
        data={"email": user_ic.email},
    )
    assert response.status_code == 204, (
        "Une response 204 est attendue (utilisateur avec IC trouvé)"
    )


def test_authenticate_with_link(client):
    # Redirection vers l'accueil si le code fourni est invalide
    response = client.get(
        reverse("authenticate_with_link", kwargs={"sesame": "foo"}),
    )
    assert response.status_code == 302, "Une redirection est attendue"
    assert response.url == settings.FRONTEND_URL, (
        "En cas d'échec, on doit rediriger vers l'accueil"
    )

    # Redirection vers l'identification du frontend si le code fourni est valide
    user = make_user(is_active=True)

    response = client.get(
        reverse(
            "authenticate_with_link", kwargs={"sesame": sesame.utils.get_token(user)}
        ),
    )
    assert response.status_code == 302, "Une redirection est attendue"
    assert "auth/pc-callback" in response.url, (
        "On doit rediriger vers l'idetification du frontend"
    )


def test_authenticate_with_link_sets_cookie(client):
    """authenticate_with_link définit le cookie d'authentification."""
    user = make_user(is_active=True)
    token, _ = Token.objects.get_or_create(user=user)

    response = client.get(
        reverse(
            "authenticate_with_link", kwargs={"sesame": sesame.utils.get_token(user)}
        ),
    )

    assert response.status_code == 302

    cookie = response.cookies["token"]
    assert cookie.value == token.key


def test_authenticate_with_link_creates_token_if_not_exists(client):
    """authenticate_with_link crée un token s'il n'en existe pas."""
    user = make_user(is_active=True)

    Token.objects.filter(user=user).delete()

    response = client.get(
        reverse(
            "authenticate_with_link", kwargs={"sesame": sesame.utils.get_token(user)}
        ),
    )

    assert response.status_code == 302
    assert Token.objects.filter(user=user).exists()
    token = Token.objects.get(user=user)
    assert response.cookies["token"].value == token.key
