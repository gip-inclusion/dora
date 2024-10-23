import enum


class Tag(enum.StrEnum):
    # liste des tags possibles pour l'analytics custom
    PAGEVIEW = "pageview"
    SEARCH = "search"
    STRUCTURE = "structure"
    STRUCTURE_INFOS = "structure_infos"
    SERVICE = "service"
    DI_SERVICE = "di_service"
    ORIENTATION = "orientation"
    SHARE = "share"
    MOBILISATION = "mobilisation"
    DI_MOBILISATION = "di_mobilisation"
