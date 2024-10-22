from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import set_rollback


def custom_exception_handler(exc, context):
    # based on rest_framework.views.exception_handler

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.get_full_details()
        else:
            data = {"detail": exc.get_full_details()}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, ValidationError):
        data = {
            "non_field_errors": [
                {
                    "code": e.code,
                    "message": e.message % e.params if e.params else e.message,
                }
                for e in exc.error_list
            ]
        }

        set_rollback()
        return Response(data, status=400)
    return None
