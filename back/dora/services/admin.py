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

from .csv_import import ImportServicesHelper
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
        self.default_source_label = "DORA"
        self.upload_size_limit_in_bytes = 10 * 1024 * 1024  # 10 MB
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
            "title": "Module d'import de services",
            "opts": self.model._meta,
            "has_view_permission": True,
            "csv_headers": ImportServicesHelper.CSV_HEADERS,
        }
        return render(request, "admin/import_services.html", context)

    def _handle_import_post(self, request):
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            messages.error(request, "Veuillez sélectionner un fichier CSV.")
            return redirect(".")

        if not csv_file.name.lower().endswith(".csv"):
            messages.error(
                request,
                mark_safe(
                    "<b>Échec de l'import - Format de fichier non valide</b><br/>"
                    "Le fichier n'est pas au format CSV attendu. Assurez-vous d'utiliser un fichier .csv avec des colonnes séparées par des virgules.",
                ),
            )
            return redirect(".")

        if csv_file.size > self.upload_size_limit_in_bytes:
            messages.error(
                request,
                "<b>Échec de l'import - Fichier trop volumineux</b><br/>Le fichier doit être moins de 10MB.",
            )
            return redirect(".")

        try:
            is_wet_run = request.POST.get("test_run") != "on"
            source_label = request.POST.get(
                "source_label", self.default_source_label
            ).strip()
            should_remove_instructions_from_csv = (
                request.POST.get("should_remove_instructions") == "on"
            )

            source_info = {
                "value": csv_file.name.rsplit(".", 1)[0],
                "label": source_label or self.default_source_label,
            }

            reader = csv.reader(io.TextIOWrapper(csv_file, encoding="utf-8"))
            result = self.import_service_helper.import_services(
                reader,
                request.user,
                source_info,
                wet_run=is_wet_run,
                should_remove_first_two_lines=should_remove_instructions_from_csv,
            )

            return self._handle_import_results(request, result, is_wet_run)

        except UnicodeDecodeError:
            messages.error(
                request,
                mark_safe(
                    "<b>Échec de l'import - Erreur d'encodage du fichier</b><br/>"
                    "Le fichier contient des caractères spéciaux illisibles. Sauvegardez votre fichier en UTF-8 et relancez l'import.",
                ),
            )
            return redirect(".")
        except Exception as e:
            messages.error(
                request,
                mark_safe(
                    "<b>Échec de l'import - Erreur inattendue</b><br/>"
                    "L'erreur suivante s'est produite :<br/>"
                    f"{e}<br/>"
                    "Si le même problème arrive, envoyez un message aux développeurs.",
                ),
            )
            return redirect(".")

    def _handle_import_results(self, request, result, is_wet_run):
        created_count = result.get("created_count", 0)
        no_errors = not result.get("missing_headers", []) and not result.get(
            "errors", []
        )

        self._add_error_messages(request, result, is_wet_run)
        self._add_warning_messages(request, result, is_wet_run)

        total_services_published = created_count - len(
            result.get("draft_services_created", [])
        )

        if is_wet_run and no_errors:
            messages.success(
                request,
                mark_safe(
                    f"<b>Import terminé avec succès</b><br/>{total_services_published} nouveaux services ont été créés et publiés"
                ),
            )
            return redirect("..")

        if not is_wet_run and no_errors:
            messages.success(
                request,
                mark_safe(
                    f"<b>Test réalisé avec succès - aucune erreur détectée</b><br/>C'est tout bon ! {total_services_published} sont prêts à être importés et publiés."
                ),
            )

        return redirect(".")

    def _add_error_messages(self, request, result, is_wet_run):
        missing_headers = result.get("missing_headers", [])
        errors = result.get("errors", [])

        if missing_headers:
            headers_list = "<br/>".join(f"• {header}" for header in missing_headers)
            message = f"<b>Échec de l'import - Colonnes manquantes</b><br/>Votre fichier CSV ne contient pas toutes les colonnes requises. Ajoutez les colonnes suivantes :<br/>{headers_list}"

            messages.error(request, mark_safe(message))

        if errors:
            error_list = "<br/>".join(f"• {error}" for error in errors)
            title_prefix = "Échec de l'import" if is_wet_run else "Test terminé"
            messages.error(
                request,
                mark_safe(
                    f"<b>{title_prefix} - Erreurs à corriger</b><br/>Le fichier contient des erreurs qui empêchent l'import. Veuillez corriger les éléments suivants :<br/>"
                    f"{error_list}",
                ),
            )

    def _add_warning_messages(self, request, result, is_wet_run):
        duplicated_services = result.get("duplicated_services", [])
        geo_data_missing = result.get("geo_data_missing_lines", [])
        draft_services_created = result.get("draft_services_created", [])

        title_prefix = "Import réalisé" if is_wet_run else "Test terminé"
        if duplicated_services:
            duplicate_list = "<br/>".join(
                f'• [{service["idx"]}] SIRET {service["siret"]} - il existe déjà un service avec le modèle {service["model_slug"]} et le courriel "{service["contact_email"]}"'
                for service in duplicated_services
            )
            messages.warning(
                request,
                mark_safe(
                    f"<b>{title_prefix} - Doublons potentiels détectés</b><br/>Nous avons détecté des similitudes avec des services existants. Nous vous recommandons de vérifier :<br/>"
                    f"{duplicate_list}"
                ),
            )

        if geo_data_missing:
            missing_list = "<br/>".join(
                f"• [{item.get('idx', '?')}] {item.get('address', '')} {item.get('postal_code', '')} {item.get('city', '')}"
                for item in geo_data_missing
            )
            messages.warning(
                request,
                mark_safe(
                    f"<b>{title_prefix} - Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                    f"{missing_list}"
                ),
            )

        if draft_services_created:
            draft_list = "<br/>".join(
                f'• [{service["idx"]}] Service "{service["name"]}" - Manque : {", ".join(service["missing_fields"])}'
                for service in draft_services_created
            )

            wet_run_message = f"<b>{title_prefix} - Services importés en brouillon</b><br/>{len(draft_services_created)} services ont été importés en brouillon. Contactez les structures pour compléter ces éléments avant publication"
            test_run_message = f"<b>{title_prefix} - Services incomplets</b><br/>{len(draft_services_created)} services seront passés en brouillon en cas d'import. Contactez les structures pour compléter ces éléments avant importation"
            message = wet_run_message if is_wet_run else test_run_message
            messages.warning(
                request,
                mark_safe(message + f" :<br/>{draft_list}"),
            )

    def remove_first_two_lines(csv_content: str) -> str:
        lines = csv_content.strip().split("\n")

        if len(lines) <= 2:
            return ""

        return "\n".join(lines[2:])


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
