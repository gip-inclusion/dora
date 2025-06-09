from data_inclusion.schema import Profil
from django import forms
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.contrib.gis import admin

from dora.core.admin import EnumAdmin

from .models import (
    AccessCondition,
    BeneficiaryAccessMode,
    Bookmark,
    CoachOrientationMode,
    ConcernedPublic,
    Credential,
    FranceTravailOrientableService,
    FundingLabel,
    LocationKind,
    Requirement,
    SavedSearch,
    Service,
    ServiceCategory,
    ServiceKind,
    ServiceModel,
    ServiceModificationHistoryItem,
    ServiceSource,
    ServiceStatusHistoryItem,
    ServiceSubCategory,
)


class ServiceModificationHistoryItemInline(admin.TabularInline):
    model = ServiceModificationHistoryItem
    readonly_fields = ["user", "date", "fields", "service", "status"]
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


class ServiceModificationHistoryItemAdmin(admin.ModelAdmin):
    list_display = ("service", "date", "user", "status")
    date_hierarchy = "date"
    list_filter = ("status",)
    readonly_fields = ["user", "date", "fields", "service", "status"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ServiceStatusHistoryItemInline(admin.TabularInline):
    model = ServiceStatusHistoryItem
    readonly_fields = ["user", "date", "new_status", "previous_status", "service"]
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


class ServiceStatusHistoryItemAdmin(admin.ModelAdmin):
    list_display = ("service", "date", "user", "new_status", "previous_status")
    date_hierarchy = "date"
    readonly_fields = ["user", "date", "new_status", "previous_status", "service"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ServiceAdmin(admin.GISModelAdmin):
    search_fields = ("name", "structure__name", "slug", "data_inclusion_id")
    list_display = [
        "name",
        "slug",
        "structure",
        "creation_date",
        "modification_date",
        "publication_date",
        "last_editor",
        "status",
    ]
    list_filter = [
        "status",
        "creation_date",
        "moderation_status",
        "source",
        "use_inclusion_numerique_scheme",
        "structure__department",
    ]
    filter_horizontal = [
        "categories",
        "subcategories",
        "access_conditions",
        "concerned_public",
        "requirements",
        "credentials",
    ]
    inlines = [ServiceStatusHistoryItemInline, ServiceModificationHistoryItemInline]
    ordering = ["-modification_date"]
    save_as = True
    readonly_fields = (
        "creation_date",
        "status",
        "data_inclusion_id",
        "data_inclusion_source",
    )
    raw_id_fields = ["structure", "model", "creator", "last_editor"]


class ServiceModelAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "structure__name",
        "slug",
    )
    list_display = [
        "name",
        "slug",
        "structure",
        "creation_date",
        "modification_date",
        "publication_date",
        "last_editor",
    ]
    list_filter = [
        ("structure", RelatedOnlyFieldListFilter),
    ]
    filter_horizontal = [
        "categories",
        "subcategories",
        "access_conditions",
        "concerned_public",
        "requirements",
        "credentials",
    ]
    inlines = [ServiceModificationHistoryItemInline]
    ordering = ["-modification_date"]
    save_as = True
    readonly_fields = ("creation_date", "modification_date", "status")
    raw_id_fields = ["structure", "model", "creator", "last_editor"]


class CustomizableChoiceAdmin(admin.ModelAdmin):
    list_display = ("name", "structure")
    list_filter = [
        ("structure", RelatedOnlyFieldListFilter),
    ]
    search_fields = (
        "name",
        "structure__name",
    )
    list_per_page = 1000
    raw_id_fields = ["structure"]


class ConcernedPublicForm(forms.ModelForm):
    profile_families = forms.MultipleChoiceField(
        choices=((p.value, p.label) for p in Profil),
        widget=forms.SelectMultiple(attrs={"size": "10"}),
        label="Familles de profils",
    )

    class Meta:
        model = ConcernedPublic
        fields = "__all__"


class ConcernedPublicAdmin(CustomizableChoiceAdmin):
    form = ConcernedPublicForm
    list_display = ("name", "get_profile_families", "structure")

    def get_profile_families(self, obj):
        return ", ".join(Profil(p).label for p in obj.profile_families)

    get_profile_families.short_description = "Familles de profils"


class ServiceModelInline(admin.TabularInline):
    model = ServiceModel
    show_change_link = True
    fields = [
        "slug",
        "name",
        "structure",
    ]
    readonly_fields = ["slug", "name", "structure"]
    extra = 0


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("creation_date", "user", "service", "di_id")
    raw_id_fields = ["user", "service"]
    readonly_fields = ["creation_date"]
    ordering = ["-creation_date"]


class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ("creation_date", "user", "category", "last_notification_date")
    raw_id_fields = ["user"]
    filter_horizontal = [
        "subcategories",
        "kinds",
        "fees",
    ]
    readonly_fields = ["creation_date"]
    ordering = ["-creation_date"]


class FranceTravailOrientableServiceAdmin(admin.ModelAdmin):
    list_display = ("created_at", "structure", "service")
    search_fields = ("structure__name", "service__name")
    list_filter = ("created_at", "structure")
    raw_id_fields = ["structure", "service"]


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceModel, ServiceModelAdmin)
admin.site.register(AccessCondition, CustomizableChoiceAdmin)
admin.site.register(ConcernedPublic, ConcernedPublicAdmin)
admin.site.register(Requirement, CustomizableChoiceAdmin)
admin.site.register(Credential, CustomizableChoiceAdmin)
admin.site.register(ServiceModificationHistoryItem, ServiceModificationHistoryItemAdmin)
admin.site.register(ServiceStatusHistoryItem, ServiceStatusHistoryItemAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(SavedSearch, SavedSearchAdmin)

admin.site.register(BeneficiaryAccessMode, EnumAdmin)
admin.site.register(CoachOrientationMode, EnumAdmin)
admin.site.register(LocationKind, EnumAdmin)
admin.site.register(ServiceCategory, EnumAdmin)
admin.site.register(ServiceKind, EnumAdmin)
admin.site.register(ServiceSubCategory, EnumAdmin)
admin.site.register(ServiceSource, EnumAdmin)
admin.site.register(FundingLabel, EnumAdmin)

admin.site.register(FranceTravailOrientableService, FranceTravailOrientableServiceAdmin)
