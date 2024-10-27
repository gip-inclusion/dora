from uuid import uuid4

import sesame.utils
from django.conf import settings
from django.shortcuts import reverse

from dora.core.test_utils import make_user

# note : utilisation de `client` et pas `api_client`

# note : inutile de tester la durée de validité et l'usage unique,
# c'est de la response de `django-sesame`


def test_send_link(client):
    # aucun lien n'est envoyé si l'utilisateur n'a pas un compte IC
    user_no_ic = make_user()
    response = client.post(
        reverse("send_link"),
        data={"email": user_no_ic.email},
    )
    assert (
        response.status_code == 404
    ), "Une response 404 est attendue (utilisateur sans IC)"

    # on vérifie qu'un lien est envoyé si l'utilisateur à un compte IC
    user_ic = make_user(ic_id=uuid4(), is_active=True)

    response = client.post(
        reverse("send_link"),
        data={"email": user_ic.email},
    )
    assert (
        response.status_code == 204
    ), "Une response 204 est attendue (utilisateur avec IC trouvé)"


def test_authenticate_with_link(client):
    # Redirection vers l'accueil si le code fourni est invalide
    response = client.get(
        reverse("authenticate_with_link", kwargs={"sesame": "foo"}),
    )
    assert response.status_code == 302, "Une redirection est attendue"
    assert (
        response.url == settings.FRONTEND_URL
    ), "En cas d'échec, on doit rediriger vers l'accueil"

    # Redirection vers l'identification du frontend si le code fourni est valide
    user = make_user(ic_id=uuid4(), is_active=True)

    response = client.get(
        reverse(
            "authenticate_with_link", kwargs={"sesame": sesame.utils.get_token(user)}
        ),
    )
    assert response.status_code == 302, "Une redirection est attendue"
    assert (
        "auth/pc-callback" in response.url
    ), "On doit rediriger vers l'idetification du frontend"
