from django.conf import settings
from rest_framework.authentication import TokenAuthentication


class CookieTokenAuthentication(TokenAuthentication):
    """Authenticates requests using the auth token stored in an httponly cookie."""

    def authenticate(self, request):
        token = request.COOKIES.get(settings.AUTH_COOKIE_NAME)
        if not token:
            return None
        return self.authenticate_credentials(token)