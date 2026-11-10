from itoutils.django.logging import DataDogJSONFormatter as ItouDataDogJSONFormatter

from dora.core.throttling import get_client_ip


class DataDogJSONFormatter(ItouDataDogJSONFormatter):
    """Formateur JSON des logs, avec l'IP réelle du client.

    Le formateur d'origine retient la première adresse de `X-Forwarded-For`,
    que le client peut falsifier lorsqu'il appelle l'API directement.
    """

    def json_record(self, message, extra, record):
        log_entry_dict = super().json_record(message, extra, record)
        if "network.client.ip" in log_entry_dict:
            wsgi_request = self.get_wsgi_request()
            if wsgi_request is not None:
                log_entry_dict["network.client.ip"] = get_client_ip(wsgi_request)
        return log_entry_dict
