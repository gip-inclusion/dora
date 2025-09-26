import logging
import threading
import time
import uuid

_thread_locals = threading.local()
logger = logging.getLogger("dora.requests")


def get_current_request():
    return getattr(_thread_locals, "request", None)


def set_current_request(request):
    _thread_locals.request = request


PRO_CONNECT_URL_ROOT = "/oidc/"


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        request = get_current_request()

        if request and not request.path.startswith(PRO_CONNECT_URL_ROOT):
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                record.ip_address = x_forwarded_for.split(",")[0].strip()
            else:
                record.ip_address = request.META.get("REMOTE_ADDR", "unknown")

            record.request_id = getattr(request, "id", "no-request-id")

            if (
                hasattr(request, "user")
                and hasattr(request.user, "id")
                and request.user.id is not None
            ):
                record.user_id = str(request.user.id)
            else:
                record.user_id = "anonymous"
        elif request and request.path.startswith(PRO_CONNECT_URL_ROOT):
            record.ip_address = request.META.get("REMOTE_ADDR", "unknown")
            record.request_id = getattr(request, "id", "no-request-id")
            record.user_id = "authenticating"
        else:
            record.ip_address = "no-request"
            record.request_id = "no-request"
            record.user_id = "no-request"

        return True


class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, "id"):
            request.id = str(uuid.uuid4())

        set_current_request(request)

        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        logger.info(
            f'"{request.method} {request.get_full_path()}" '
            f"{response.status_code} {duration * 1000:.0f}ms"
        )

        return self.get_response(request)
