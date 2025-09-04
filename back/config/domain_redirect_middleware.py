from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class DomainRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        old_host = getattr(settings, "OLD_HOST", None)
        new_host = getattr(settings, "NEW_HOST", None)

        if not old_host or not new_host:
            return None

        current_host = request.get_host()

        if current_host == old_host:
            new_url = f"https://{new_host}{request.get_full_path()}"

            response = HttpResponseRedirect(new_url, preserve_request=True)
            return response

        return None
