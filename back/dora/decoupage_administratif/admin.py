from django.contrib import admin

from .models import Commune, Departement, Epci, Region


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ("nom", "code", "code_departement", "code_epci", "code_region")
    search_fields = ("nom", "code")
    list_filter = (
        "code_departement",
        "code_epci",
        "code_region",
    )
    readonly_fields = (
        "nom",
        "code",
        "code_departement",
        "code_epci",
        "code_region",
        "codes_postaux",
    )


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ("nom", "code", "code_region")
    search_fields = ("nom", "code")
    list_filter = ("code_region",)
    readonly_fields = ("nom", "code", "code_region")


@admin.register(Epci)
class EpciAdmin(admin.ModelAdmin):
    list_display = ("nom", "code", "codes_departements", "codes_regions")
    search_fields = ("nom", "code")
    readonly_fields = ("nom", "code", "codes_departements", "codes_regions")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("nom", "code")
    search_fields = ("nom", "code")
    readonly_fields = ("nom", "code")
