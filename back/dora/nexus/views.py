import logging
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from dora.nexus.utils import decode_jwt

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def auto_login_in(request):
    token = request.data.get("jwt")
    next_url = request.data.get("next")

    email = None
    try:
        claims = decode_jwt(token)
        email = claims.get("email")
    except ValueError:
        logger.info("Nexus auto login: Invalid auto login token")

    if email is None:
        logger.info("Nexus auto login: Missing email in token -> ignored")
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.user.is_authenticated and request.user.email == email:
        logger.info("Nexus auto login: User is already logged in")
        return Response(status=status.HTTP_204_NO_CONTENT)

    params = {}
    if next_url:
        params["next"] = next_url
    if email:
        params["login_hint"] = email

    authorize_url = reverse("oidc_authentication_init")
    if params:
        authorize_url += "?" + urlencode(params)
    absolute_authorize_url = request.build_absolute_uri(authorize_url)

    absolute_logout_url = f"{settings.FRONTEND_URL}/auth/pc-logout/"

    redirect_url = (
        absolute_logout_url if request.user.is_authenticated else absolute_authorize_url
    )

    return Response({"redirect_url": redirect_url}, status=status.HTTP_200_OK)
