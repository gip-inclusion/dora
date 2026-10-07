from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle


class UploadRateThrottle(UserRateThrottle):
    """Throttle spécifique pour les endpoints du chargement de fichiers."""

    scope = "upload"


class OrientationsExportLinkThrottle(UserRateThrottle):
    """Throttle pour l'envoi par e-mail du lien d'export des orientations."""

    scope = "orientations_export_link"


class StructureUploadThrottle(SimpleRateThrottle):
    """Throttle par structure pour éviter l'abus d'une structure compromise."""

    scope = "structure_upload"

    def get_cache_key(self, request, view):
        structure_slug = request.resolver_match.kwargs["structure_slug"]
        return self.cache_format % {"scope": self.scope, "ident": structure_slug}
