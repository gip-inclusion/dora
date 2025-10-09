import logging

from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from dora.core.admin import EnumAdmin
from dora.core.models import ModerationStatus
from dora.orientations.emails import send_orientation_created_emails
from dora.orientations.models import Orientation, OrientationStatus
from dora.services.models import Service
from dora.structures.emails import send_moderation_rejected_notification

from ..core.mixins import BaseImportAdminMixin
from .csv_import import ImportStructuresHelper
from .models import (
    DisabledDoraFormDIStructure,
    Structure,
    StructureMember,
    StructureNationalLabel,
    StructurePutativeMember,
    StructureSource,
)

logger = logging.getLogger("dora.logs.core")


class StructurePutativeMemberAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "structure__name",
        "structure__department",
    )

    list_display = [
        "user",
        "structure",
        "is_admin",
        "invited_by_admin",
        "creation_date",
    ]
    list_filter = [
        "is_admin",
        "invited_by_admin",
        ("structure", RelatedOnlyFieldListFilter),
    ]

    ordering = ["-creation_date"]
    raw_id_fields = ["user", "structure"]


class StructureMemberAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "structure__name",
        "structure__department",
    )

    list_display = [
        "user",
        "structure",
        "is_admin",
        "creation_date",
    ]
    list_filter = [
        "is_admin",
        ("structure", RelatedOnlyFieldListFilter),
    ]

    ordering = ["-creation_date"]
    raw_id_fields = ["user", "structure"]


class StructureMemberInline(admin.TabularInline):
    model = StructureMember
    show_change_link = True
    extra = 0
    raw_id_fields = ["user", "structure"]
    raw_id_fields = ["user"]


class StructurePutativeMemberInline(admin.TabularInline):
    model = StructurePutativeMember
    show_change_link = True
    extra = 0
    raw_id_fields = ["user"]


class BranchFormSet(BaseInlineFormSet):
    def save_new_objects(self, commit=True):
        saved_instances = super().save_new_objects(commit)

        if commit and saved_instances:
            for instance in saved_instances:
                instance.parent.post_create_branch(
                    instance,
                    self.request.user,
                    StructureSource.objects.get(value="porteur"),
                )
        return saved_instances


class BranchInline(admin.TabularInline):
    model = Structure
    show_change_link = True
    formset = BranchFormSet
    fields = [
        "name",
        "siret",
    ]
    extra = 1
    verbose_name = "Antenne"
    verbose_name_plural = "Antennes"
    show_change_link = True

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.request = request
        return formset

    def has_add_permission(self, request, obj):
        return obj.parent is None if obj else True

    def save_formset(self, request, form, formset, change):
        formset.save()


class ModerationPendingListFilter(admin.SimpleListFilter):
    title = "statut de modération"
    parameter_name = "pending_moderation"

    def lookups(self, request, model_admin):
        return (("pending_moderation", "À modérer"),)

    def queryset(self, request, queryset):
        if self.value() == "pending_moderation":
            return queryset.filter(
                orientations__status=OrientationStatus.MODERATION_PENDING
            ).distinct()


class IsBranchListFilter(admin.SimpleListFilter):
    title = "antenne"
    parameter_name = "is_branch"

    def lookups(self, request, model_admin):
        return (
            ("false", "Non"),
            ("true", "Oui"),
        )

    def queryset(self, request, queryset):
        if self.value() == "false":
            return queryset.filter(parent__isnull=True)
        if self.value() == "true":
            return queryset.filter(parent__isnull=False)


class ServiceInline(admin.TabularInline):
    model = Service
    show_change_link = True
    fields = ["slug", "name", "status"]
    extra = 0


class OrientationModerationPendingInline(admin.TabularInline):
    model = Orientation
    verbose_name = "Orientation en cours de modération"
    verbose_name_plural = "Orientations en cours de modération"
    show_change_link = True
    can_delete = False
    extra = 0
    fields = [
        "beneficiary_first_name",
        "beneficiary_last_name",
        "beneficiary_email",
        "referent_first_name",
        "referent_last_name",
        "referent_email",
        "service",
        "di_service_id",
        "orientation_reasons",
    ]
    readonly_fields = [
        "beneficiary_first_name",
        "beneficiary_last_name",
        "beneficiary_email",
        "referent_first_name",
        "referent_last_name",
        "referent_email",
        "service",
        "di_service_id",
        "orientation_reasons",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=OrientationStatus.MODERATION_PENDING)

    def has_add_permission(self, request, obj=None):
        return False


class StructureAdmin(BaseImportAdminMixin, admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        self.import_structure_helper = ImportStructuresHelper()
        return super().__init__(*args, **kwargs)

    list_display = [
        "name",
        "slug",
        "parent",
        "department",
        "typology",
        "city_code",
        "city",
        "creation_date",
        "modification_date",
        "last_editor",
    ]
    list_filter = [
        ModerationPendingListFilter,
        IsBranchListFilter,
        "is_obsolete",
        "moderation_status",
        "creation_date",
        "modification_date",
        "source",
        "typology",
        "national_labels",
        "department",
    ]
    search_fields = (
        "name",
        "siret",
        "code_safir_ft",
        "city",
        "department",
        "slug",
        "data_inclusion_id",
    )

    inlines = [
        StructureMemberInline,
        StructurePutativeMemberInline,
        BranchInline,
        ServiceInline,
        OrientationModerationPendingInline,
    ]
    readonly_fields = (
        "creation_date",
        "modification_date",
        "data_inclusion_id",
        "data_inclusion_source",
    )
    raw_id_fields = ("parent", "creator", "last_editor")

    # Ajout du contexte moderation_pending qui définit si oui ou non le bloc modération est affiché.
    def change_view(self, request, object_id, form_url="", extra_context=None):
        structure = self.get_object(request, object_id)
        extra_context = extra_context or {}
        extra_context["moderation_pending"] = structure.orientations.filter(
            status=OrientationStatus.MODERATION_PENDING
        ).exists()
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    # Définition de l'URL pour l'action de modération Approuver
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/moderation_approve/",
                self.admin_site.admin_view(self.moderation_approve),
                name="moderation_approve",
            ),
            path(
                "<path:object_id>/moderation_reject/",
                self.admin_site.admin_view(self.moderation_reject),
                name="moderation_reject",
            ),
            path(
                "import-structures/",
                self.admin_site.admin_view(self.import_structures_view),
                name="structures_structure_import",
            ),
            path(
                "import-job-status/<uuid:job_id>/",
                self.admin_site.admin_view(self.import_job_status),
                name="structures_import_job_status",
            ),
        ]
        return custom_urls + urls

    def is_moderation_pending(self, structure):
        return structure.orientations.filter(
            status=OrientationStatus.MODERATION_PENDING
        ).exists()

    def get_moderation_pending_structure_list_url(self):
        structure_list_url = reverse("admin:structures_structure_changelist")
        return f"{structure_list_url}?pending_moderation=pending_moderation"

    # Action de modération Approuver
    def moderation_approve(self, request, object_id):
        structure = self.get_object(request, object_id)

        # Si la structure n'est plus en attente de modération, on redirige vers la liste des structures en attente de modération
        if not self.is_moderation_pending(structure):
            self.message_user(
                request,
                f"Le rattachement à la structure « {structure} » n’est pas (ou plus) en attente de modération. Votre action a été ignorée.",
            )
            return HttpResponseRedirect(
                self.get_moderation_pending_structure_list_url()
            )

        moderation_pending_orientations = structure.orientations.filter(
            status=OrientationStatus.MODERATION_PENDING
        )

        logger.info(
            "Modération de structure : approbation",
            {
                "legal": False,
                "userId": str(request.user.pk),
                "userEmail": request.user.email,
                "structureId": str(structure.pk),
                "orientationIds": [
                    str(orientation.pk)
                    for orientation in moderation_pending_orientations
                ],
            },
        )

        # Passage de la structure au statut de modération Validé
        structure.moderation_status = ModerationStatus.VALIDATED
        structure.save()

        # Passage des demandes d'orientation en attente au statut Ouverte / En cours de traitement et envoi des e-mails
        for orientation in moderation_pending_orientations:
            orientation.status = OrientationStatus.PENDING
            orientation.save()
            send_orientation_created_emails(orientation)

        # Message de confirmation
        self.message_user(
            request,
            f"Le rattachement à la structure « {structure} » a été approuvé. Les demandes d’orientation en attente ont été transmises.",
        )

        # Redirection vers la liste des structures en attente de modération
        return HttpResponseRedirect(self.get_moderation_pending_structure_list_url())

    # Action de modération Rejeter
    def moderation_reject(self, request, object_id):
        structure = self.get_object(request, object_id)

        # Si la structure n'est plus en attente de modération, on redirige vers la liste des structures en attente de modération
        if not self.is_moderation_pending(structure):
            self.message_user(
                request,
                f"Le rattachement à la structure « {structure} » n’est pas (ou plus) en attente de modération. Votre action a été ignorée.",
            )
            return HttpResponseRedirect(
                self.get_moderation_pending_structure_list_url()
            )

        reason = request.POST.get("reason")

        moderation_pending_orientations = structure.orientations.filter(
            status=OrientationStatus.MODERATION_PENDING
        )

        logger.info(
            "Modération de structure : rejet",
            {
                "legal": False,
                "userId": str(request.user.pk),
                "userEmail": request.user.email,
                "structureId": str(structure.pk),
                "orientationIds": [
                    str(orientation.pk)
                    for orientation in moderation_pending_orientations
                ],
                "memberIds": [str(member.pk) for member in structure.members.all()],
                "putativeMemberIds": [
                    str(putative_member.pk)
                    for putative_member in structure.putative_members.all()
                ],
                "reason": reason,
            },
        )

        # Envoi d'un e-mail explicatif à tous les membres et membres potentiels
        send_moderation_rejected_notification(structure, reason)

        # Désactivation de tous les membres et membres potentiels de la structure
        structure.members.update(is_active=False)
        structure.putative_members.update(is_active=False)

        # Détachement de tous les membres et membres potentiels de la structure
        structure.members.clear()
        structure.putative_members.clear()

        # Passage de la structure au statut de modération Nouvelle modération nécessaire
        structure.moderation_status = ModerationStatus.NEED_NEW_MODERATION
        structure.moderation_date = timezone.now()
        structure.save()

        # Passage des demandes d'orientation en cours de modération au statut Supprimée par la modération
        moderation_pending_orientations.update(
            status=OrientationStatus.MODERATION_REJECTED
        )

        # Message de confirmation
        self.message_user(
            request,
            f"Le rattachement à la structure « {structure} » a été rejeté. Les demandes d’orientation en attente ont été supprimées.",
        )

        # Redirection vers la liste des structures en attente de modération
        return HttpResponseRedirect(self.get_moderation_pending_structure_list_url())

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["import_url"] = "import-structures/"
        return super().changelist_view(request, extra_context)

    def import_structures_view(self, request):
        if request.method == "POST":
            return self.import_csv(request)

        context = {
            "title": "Module d'import de structures",
            "opts": self.model._meta,
            "has_view_permission": True,
            "csv_headers": ImportStructuresHelper.CSV_HEADERS,
        }
        return render(request, "admin/import_csv_form.html", context)

    def format_results(self, result, is_wet_run):
        messages = []
        errors_map = result.get("errors_map", {})
        created_structures_count = result.get("created_structures_count", 0)
        created_services_count = result.get("created_services_count", 0)
        edited_structures_count = result.get("edited_structures_count", 0)

        if not errors_map and is_wet_run:
            messages.append(
                {
                    "level": "success",
                    "message": format_html(
                        f"<b>Import terminé avec succès</b><br/>{created_structures_count} nouvelles structures ont été créées.<br/>"
                        f"{edited_structures_count} structures existantes ont été modifiées.<br/>"
                        f"{created_services_count} nouveaux services ont été crées en brouillon.<br/>"
                    ),
                }
            )

        elif not errors_map and not is_wet_run:
            messages.append(
                {
                    "level": "success",
                    "message": format_html(
                        "<b>Import de test terminé avec succès</b><br/>"
                    ),
                }
            )

        elif errors_map:
            error_messages = []
            for line, errors in errors_map.items():
                error_messages.append(f"[{line}]: {', '.join(errors)}")

            title_prefix = "Échec de l'import" if is_wet_run else "Test terminé"

            messages.append(
                {
                    "level": "error",
                    "message": format_html(
                        f"<b>{title_prefix} - Erreurs rencontrées</b><br/>"
                        f"{('<br/>').join(error_messages)}"
                    ),
                }
            )

        return messages

    def get_import_helper(self):
        return self.import_structure_helper

    def get_import_method_name(self):
        return "import_structures"

    def get_import_type_name(self):
        return "structures"

    def get_import_title(self):
        return "Module d'import de structures"

    def get_csv_headers(self):
        return ImportStructuresHelper.CSV_HEADERS


class DisabledDoraFormDIStructureAdmin(admin.ModelAdmin):
    list_display = ["source", "structure_id", "comment"]
    search_fields = ["source", "structure_id", "comment"]


admin.site.register(Structure, StructureAdmin)
admin.site.register(StructureMember, StructureMemberAdmin)
admin.site.register(StructurePutativeMember, StructurePutativeMemberAdmin)
admin.site.register(StructureSource, EnumAdmin)
admin.site.register(StructureNationalLabel, EnumAdmin)
admin.site.register(DisabledDoraFormDIStructure, DisabledDoraFormDIStructureAdmin)
