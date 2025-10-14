from data_inclusion.schema.v1.publics import Public as DiPublic
from django import forms
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.contrib.gis import admin
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html

from dora.core.admin import EnumAdmin

from ..core.mixins import BaseImportAdminMixin
from .csv_import import ImportServicesHelper
from .models import (
    AccessCondition,
    BeneficiaryAccessMode,
    Bookmark,
    CoachOrientationMode,
    Credential,
    FranceTravailOrientableService,
    FundingLabel,
    LocationKind,
    Public,
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


class ServiceAdmin(BaseImportAdminMixin, admin.GISModelAdmin):
    def __init__(self, *args, **kwargs):
        self.import_service_helper = ImportServicesHelper()
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
        "publics",
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
            path(
                "import-job-status/<uuid:job_id>/",
                self.admin_site.admin_view(self.import_job_status),
                name="services_import_job_status",
            ),
        ]
        return custom_urls + urls

    def import_services_view(self, request):
        if request.method == "POST":
            return self.import_csv(request)

        context = {
            "title": "Module d'import de services",
            "opts": self.model._meta,
            "has_view_permission": True,
            "csv_headers": ImportServicesHelper.CSV_HEADERS,
        }

        job_id = request.GET.get("job_id")
        if job_id:
            context["job_id"] = job_id

        return render(request, "admin/import_csv_form.html", context)

    def format_results(self, result, is_wet_run):
        success_messages = []

        created_count = result.get("created_count", 0)
        no_errors = not result.get("missing_headers", []) and not result.get(
            "errors", []
        )

        error_messages = self._add_error_messages(result, is_wet_run)
        warning_messages = self._add_warning_messages(result, is_wet_run)

        total_services_published = created_count - len(
            result.get("draft_services_created", [])
        )

        if is_wet_run and no_errors:
            success_messages.append(
                {
                    "level": "success",
                    "message": format_html(
                        f"<b>Import terminé avec succès</b><br/>{total_services_published} nouveaux services ont été créés et publiés"
                    ),
                }
            )

        if not is_wet_run and no_errors:
            success_messages.append(
                {
                    "level": "success",
                    "message": format_html(
                        f"<b>Test réalisé avec succès - aucune erreur détectée</b><br/>C'est tout bon ! {total_services_published} sont prêts à être importés et publiés."
                    ),
                }
            )

        return success_messages + error_messages + warning_messages

    def _add_error_messages(self, result, is_wet_run):
        missing_headers = result.get("missing_headers", [])
        errors = result.get("errors", [])

        messages = []

        if missing_headers:
            headers_list = "<br/>".join(f"• {header}" for header in missing_headers)
            message = f"<b>Échec de l'import - Colonnes manquantes</b><br/>Votre fichier CSV ne contient pas toutes les colonnes requises. Ajoutez les colonnes suivantes :<br/>{headers_list}"

            messages.append({"level": "error", "message": format_html(message)})

        if errors:
            error_list = "<br/>".join(f"• {error}" for error in errors)
            message_title = (
                "Échec de l'import"
                if is_wet_run
                else "Test terminé - Erreurs à corriger"
            )
            message_text = (
                "Aucun service n’a été importé, car le fichier comporte des erreurs."
                if is_wet_run
                else "Le fichier contient des erreurs qui empêcheront l'import."
            )
            messages.append(
                {
                    "level": "error",
                    "message": format_html(
                        f"<b>{message_title}</b><br/>{message_text} Veuillez corriger les éléments suivants :<br/>"
                        f"{error_list}",
                    ),
                }
            )

        return messages

    def _add_warning_messages(self, result, is_wet_run):
        duplicated_services = result.get("duplicated_services", [])
        geo_data_missing = result.get("geo_data_missing_lines", [])
        draft_services_created = result.get("draft_services_created", [])
        errors = result.get("errors", [])

        messages = []

        if (
            errors
            and is_wet_run
            and (duplicated_services or geo_data_missing or draft_services_created)
        ):
            messages.append(
                {
                    "level": "warning",
                    "message": format_html(
                        "<b>D'autres irrégularités non bloquantes ont été détectées :</b>"
                    ),
                }
            )

        title_prefix = ""
        if not errors and is_wet_run:
            title_prefix = "Import réalisé - "
        elif not is_wet_run:
            title_prefix = "Test terminé - "
        if duplicated_services:
            duplicate_list = "<br/>".join(
                f'• [{service["idx"]}] SIRET {service["siret"]} - il existe déjà un service avec le modèle {service["model_slug"]} et le courriel "{service["contact_email"]}"'
                for service in duplicated_services
            )
            messages.append(
                {
                    "level": "warning",
                    "message": format_html(
                        f"<b>{title_prefix}Doublons potentiels détectés</b><br/>Nous avons détecté des similitudes avec des services existants. Nous vous recommandons de vérifier :<br/>"
                        f"{duplicate_list}"
                    ),
                }
            )

        if geo_data_missing:
            missing_list = "<br/>".join(
                f"• [{item.get('idx', '?')}] {item.get('address', '')} {item.get('postal_code', '')} {item.get('city', '')}"
                for item in geo_data_missing
            )
            messages.append(
                {
                    "level": "warning",
                    "message": format_html(
                        f"<b>{title_prefix}Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                        f"{missing_list}"
                    ),
                }
            )

        if draft_services_created:
            draft_list = "<br/>".join(
                f'• [{service["idx"]}] Service "{service["name"]}" - Manque : {", ".join(service["missing_fields"])}'
                for service in draft_services_created
            )
            if errors and is_wet_run:
                message = "<b>Informations manquantes</b><br/> Contactez les structures pour compléter ces éléments avant importation"
            if not errors and is_wet_run:
                message = f"<b>{title_prefix}Services importés en brouillon</b><br/>{len(draft_services_created)} services ont été importés en brouillon. Contactez les structures pour compléter ces éléments avant publication"
            if not is_wet_run:
                message = f"<b>{title_prefix}Services incomplets</b><br/>{len(draft_services_created)} services seront passés en brouillon en cas d'import. Contactez les structures pour compléter ces éléments avant importation"

            messages.append(
                {
                    "level": "warning",
                    "message": format_html(message + f" :<br/>{draft_list}"),
                }
            )

        return messages

    def get_import_helper(self):
        return self.import_service_helper

    def get_import_method_name(self):
        return "import_services"

    def get_import_type_name(self):
        return "services"

    def get_import_title(self):
        return "Module d'import de services"

    def get_csv_headers(self):
        return ImportServicesHelper.CSV_HEADERS


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
        "publics",
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


class PublicForm(forms.ModelForm):
    corresponding_di_publics = forms.MultipleChoiceField(
        choices=((p.value, p.label) for p in DiPublic),
        widget=forms.SelectMultiple(attrs={"size": "10"}),
        label="Publics Data Inclusion correspondants",
    )

    class Meta:
        model = Public
        fields = "__all__"


class PublicAdmin(CustomizableChoiceAdmin):
    form = PublicForm
    list_display = ("name", "get_corresponding_di_publics", "structure")

    def get_corresponding_di_publics(self, obj):
        return ", ".join(DiPublic(p).label for p in obj.corresponding_di_publics)

    get_corresponding_di_publics.short_description = (
        "Publics Data Inclusion correspondants"
    )


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
admin.site.register(Public, PublicAdmin)
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
