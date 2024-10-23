from django.contrib.gis import admin

from .models import ServiceSuggestion


class ServiceSuggestionAdmin(admin.GISModelAdmin):
    search_fields = (
        "name",
        "siret",
    )
    list_display = [
        "name",
        "siret",
        "creation_date",
    ]
    raw_id_fields = ["creator"]


admin.site.register(ServiceSuggestion, ServiceSuggestionAdmin)
