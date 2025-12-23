from rest_framework.throttling import UserRateThrottle


class UploadRateThrottle(UserRateThrottle):
    """Throttle spécifique pour les endpoints du chargement de fichiers."""

    scope = "upload"


class StructureUploadThrottle(UserRateThrottle):
    """Throttle par structure pour éviter l'abus d'une structure compromise."""

    scope = "structure_upload"

    def get_cache_key(self, request, view):
        structure_slug = view.kwargs["structure_slug"]
        return self.cache_format % {"scope": self.scope, "ident": structure_slug}
