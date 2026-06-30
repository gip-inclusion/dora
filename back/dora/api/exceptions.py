from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE


class ServiceUnavailable(APIException):
    status_code = HTTP_503_SERVICE_UNAVAILABLE
    default_detail = (
        "Le serveur n'est pas prêt à traiter la requête, réessayez plus tard."
    )
    default_code = "service_unavailable"
