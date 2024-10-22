from django.db import models


class ServiceStatus(models.TextChoices):
    SUGGESTION = "SUGGESTION", "Suggestion"
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    ARCHIVED = "ARCHIVED", "Archived"


class ServiceUpdateStatus(models.TextChoices):
    NEEDED = "NEEDED", "Actualisation conseillée"
    NOT_NEEDED = "NOT_NEEDED", "Service à jour"
    REQUIRED = "REQUIRED", "Actualisation exigée"
