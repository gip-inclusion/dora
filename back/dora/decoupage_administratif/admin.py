from django.contrib import admin

from .models import EPCI, City, Department, Region


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "department", "epci", "region")
    search_fields = ("name", "code")
    list_filter = ("department", "region")
    readonly_fields = ("name", "code", "department", "epci", "region", "postal_codes")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "region")
    search_fields = ("name", "code")
    list_filter = ("region",)
    readonly_fields = ("name", "code", "region")


@admin.register(EPCI)
class EPCIAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "departments", "regions")
    search_fields = ("name", "code")
    readonly_fields = ("name", "code", "departments", "regions")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    readonly_fields = ("name", "code")
