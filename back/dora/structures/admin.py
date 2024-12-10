from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from dora.core.admin import EnumAdmin
from dora.core.models import ModerationStatus
from dora.orientations.emails import send_orientation_created_emails
from dora.orientations.models import Orientation, OrientationStatus
from dora.services.models import Service

from .models import (
    Structure,
    StructureMember,
    StructureNationalLabel,
    StructurePutativeMember,
    StructureSource,
)


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
        "orientation_reasons",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=OrientationStatus.MODERATION_PENDING)

    def has_add_permission(self, request, obj=None):
        return False


class StructureAdmin(admin.ModelAdmin):
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
        "code_safir_pe",
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
        ]
        return custom_urls + urls

    # Action de modération Approuver
    def moderation_approve(self, request, object_id):
        structure = self.get_object(request, object_id)

        # Passage de la structure au statut de modération Validé
        structure.moderation_status = ModerationStatus.VALIDATED
        structure.save()

        # Passage des demandes d'orientation en attente au statut Ouverte / En cours de traitement et envoi des e-mails
        moderation_pending_orientations = structure.orientations.filter(
            status=OrientationStatus.MODERATION_PENDING
        )
        for orientation in moderation_pending_orientations:
            orientation.status = OrientationStatus.PENDING
            orientation.save()
            send_orientation_created_emails(orientation)

        # Message de confirmation
        self.message_user(
            request,
            f"Le rattachement à la structure « {structure} » a été approuvé. Les demandes d’orientation en attente ont été transmises.",
        )
        return HttpResponseRedirect(
            reverse("admin:structures_structure_change", args=[object_id])
        )


admin.site.register(Structure, StructureAdmin)
admin.site.register(StructureMember, StructureMemberAdmin)
admin.site.register(StructurePutativeMember, StructurePutativeMemberAdmin)
admin.site.register(StructureSource, EnumAdmin)
admin.site.register(StructureNationalLabel, EnumAdmin)
