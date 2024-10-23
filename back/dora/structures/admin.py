from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from django.forms.models import BaseInlineFormSet

from dora.core.admin import EnumAdmin
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
    ]
    readonly_fields = (
        "creation_date",
        "modification_date",
        "data_inclusion_id",
        "data_inclusion_source",
    )
    raw_id_fields = ("parent", "creator", "last_editor")


admin.site.register(Structure, StructureAdmin)
admin.site.register(StructureMember, StructureMemberAdmin)
admin.site.register(StructurePutativeMember, StructurePutativeMemberAdmin)
admin.site.register(StructureSource, EnumAdmin)
admin.site.register(StructureNationalLabel, EnumAdmin)
