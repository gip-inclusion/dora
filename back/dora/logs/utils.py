from django_datadog_logger.formatters import datadog


class RedactUserInformationDataDogJSONFormatter(datadog.DataDogJSONFormatter):
    def json_record(self, message, extra, record):
        log_entry_dict = super().json_record(message, extra, record)
        for log_key in {"usr.name", "usr.email", "usr.session_key"}:
            if log_key in log_entry_dict:
                del log_entry_dict[log_key]
        return log_entry_dict
