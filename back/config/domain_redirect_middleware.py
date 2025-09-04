from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class DomainRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        old_domain = getattr(settings, "OLD_DOMAIN", None)
        new_domain = getattr(settings, "NEW_DOMAIN", None)

        if not old_domain or not new_domain:
            return None

        current_host = request.get_host()

        if current_host == old_domain:
            new_url = f"http://{new_domain}{request.get_full_path()}"

            response = HttpResponseRedirect(new_url)
            response.status_code = response.status_code_preserve_request
            return response

        return None
