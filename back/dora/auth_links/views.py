from django.conf import settings
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from sesame.utils import get_query_string, get_user

from dora.auth_links.emails import send_authentication_link
from dora.users.models import User


@csrf_exempt
@require_http_methods(["POST"])
def send_link(request):
    # on ne veut que des utilisateurs qui se sont déjà connectés via IC
    user = get_object_or_404(
        User,
        email=request.POST.get("email"),
        is_active=True,
        is_valid=True,
        ic_id__isnull=False,
    )

    magic_link_qs = get_query_string(user)
    url = request.build_absolute_uri(reverse("authenticate_with_link")) + magic_link_qs

    send_authentication_link(user.email, url)

    return HttpResponse(status=204)


def authenticate_with_link(request):
    if sesame := request.GET.get(settings.SESAME_TOKEN_NAME):
        if user := get_user(sesame):
            token, _ = Token.objects.get_or_create(user=user)

            # on garde une trace de la connexion par lien magique
            # pour ne pas effectuer le flow de déconnexion OIDC en entier
            request.session[settings.SESAME_SESSION_NAME] = True

            redirect_uri = f"{settings.FRONTEND_URL}/auth/pc-callback/{token}/"
            return HttpResponseRedirect(redirect_uri)

    # Le lien est invalide ou expiré
    return HttpResponse(status=403)
