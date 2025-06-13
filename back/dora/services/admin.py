import csv
import io

from data_inclusion.schema.v0 import Profil
from django import forms
from django.contrib import messages
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.contrib.gis import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.safestring import mark_safe

from dora.core.admin import EnumAdmin

from .management.commands.import_services import CSV_HEADERS, import_services
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
    def __init__(self, *args, **kwargs):
        self.default_source_label = "Importé de l'admin"
        self.upload_size_limit_in_bytes = 10 * 1024 * 1024  # 10 MB
        return super().__init__(*args, **kwargs)

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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["import_url"] = "import-services/"
        return super().changelist_view(request, extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-services/",
                self.admin_site.admin_view(self.import_services_view),
                name="services_service_import",
            ),
        ]
        return custom_urls + urls

    def import_services_view(self, request):
        if request.method == "POST":
            return self._handle_import_post(request)

        context = {
            "title": "Import Services d'un CSV",
            "opts": self.model._meta,
            "has_view_permission": True,
            "csv_headers": CSV_HEADERS,
        }
        return render(request, "admin/import_services.html", context)

    def _handle_import_post(self, request):
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            messages.error(request, "Veuillez sélectionner un fichier CSV.")
            return redirect(".")

        if not csv_file.name.lower().endswith(".csv"):
            messages.error(request, "Veuillez télécharger un fichier CSV valide.")
            return redirect(".")

        if csv_file.size > self.upload_size_limit_in_bytes:
            messages.error(request, "Le fichier est trop volumineux (maximum 10MB).")
            return redirect(".")

        try:
            is_wet_run = request.POST.get("wet_run") == "on"
            source_label = request.POST.get(
                "source_label", self.default_source_label
            ).strip()

            source_info = {
                "value": csv_file.name.rsplit(".", 1)[0],
                "label": source_label or self.default_source_label,
            }

            reader = csv.reader(io.TextIOWrapper(csv_file, encoding="utf-8"))
            result = import_services(
                reader, request.user, source_info, wet_run=is_wet_run
            )

            return self._handle_import_results(request, result, is_wet_run)

        except UnicodeDecodeError:
            messages.error(
                request,
                "Erreur d'encodage du fichier. Assurez-vous que le fichier est encodé en UTF-8.",
            )
            return redirect(".")
        except Exception as e:
            messages.error(request, f"Une erreur inattendue s'est produite : {str(e)}")
            return redirect(".")

    def _handle_import_results(self, request, result, is_wet_run):
        created_count = result.get("created_count", 0)
        errors = result.get("errors", [])
        duplicated_services = result.get("duplicated_services", [])
        geo_data_missing = result.get("geo_data_missing_lines", [])

        if is_wet_run and not errors:
            messages.success(
                request,
                f"Votre import a réussi. Vous avez créé {created_count} nouveaux services.",
            )
            self._add_warning_messages(request, duplicated_services, geo_data_missing)
            return redirect("..")

        if is_wet_run:
            messages.info(
                request, f"Import terminé avec {created_count} services créés."
            )
        else:
            messages.success(
                request,
                f"Votre import de test est fini. Vous auriez créé {created_count} nouveaux services.",
            )

        self._add_error_messages(request, errors)
        self._add_warning_messages(request, duplicated_services, geo_data_missing)

        return redirect(".")

    def _add_error_messages(self, request, errors):
        if errors:
            error_list = "<br/>".join(f"• {error}" for error in errors)
            messages.error(
                request,
                mark_safe(
                    f"Il faut résoudre les erreurs suivantes avant que vous puissiez faire l'import :<br/>"
                    f"{error_list}"
                ),
            )

    def _add_warning_messages(self, request, duplicated_services, geo_data_missing):
        if duplicated_services:
            duplicate_list = "<br/>".join(f"• {dup}" for dup in duplicated_services)
            messages.warning(
                request,
                mark_safe(
                    f"Certains services sont déjà présents dans la base de données :<br/>"
                    f"{duplicate_list}"
                ),
            )

        if geo_data_missing:
            missing_list = "<br/>".join(
                f"• Ligne {item.get('idx', '?')} - {item.get('address', 'Adresse inconnue')}"
                for item in geo_data_missing
            )
            messages.warning(
                request,
                mark_safe(
                    f"Certains services n'ont pas pu être géolocalisés :<br/>"
                    f"{missing_list}"
                ),
            )


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
