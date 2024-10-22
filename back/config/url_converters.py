class InseeCodeConverter:
    regex = r"\d[0-9aAbB]\d{3}"

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return f"{value}"


class SiretConverter:
    regex = r"\d{14}"

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return f"{value}"
