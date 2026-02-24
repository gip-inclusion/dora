import logging
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from itoutils.django.nexus.api import NexusAPIClient
from itoutils.django.nexus.token import decode_token, generate_auto_login_token
from itoutils.urls import add_url_params
from rest_framework import exceptions, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import NexusMenuStatusSerializer

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def auto_login_in(request):
    token = request.data.get("jwt")
    next_url = request.data.get("next")

    email = None
    try:
        claims = decode_token(token)
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


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def auto_login_out(request):
    next_url = request.data.get("next_url")

    if next_url is None or settings.PDI_JWT_KEY is None:
        raise exceptions.NotFound

    if url_has_allowed_host_and_scheme(
        next_url, settings.NEXUS_ALLOWED_REDIRECT_HOSTS, require_https=True
    ):
        redirect_url = add_url_params(
            next_url, {"auto_login": generate_auto_login_token(request.user)}
        )
        return Response({"redirect_url": redirect_url}, status=status.HTTP_200_OK)

    raise exceptions.NotFound


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def nexus_menu_status(request):
    if not settings.NEXUS_MENU_ENABLED:
        return Response(status=status.HTTP_204_NO_CONTENT)

    data = NexusAPIClient().dropdown_status(request.user.email)
    serializer = NexusMenuStatusSerializer(data, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)
