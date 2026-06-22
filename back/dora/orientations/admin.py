from django.contrib import admin, messages

from dora.core.models import LogItem

from .checks import check_orientation, format_warnings
from .models import EmploisOrientationData, Orientation, SentContactEmail


class EmploisOrientationDataInline(admin.StackedInline):
    model = EmploisOrientationData
    can_delete = False
    readonly_fields = (
        "beneficiary_id",
        "structure_id",
        "structure_name",
        "structure_siret",
        "prescriber_id",
        "prescriber_email",
        "prescriber_first_name",
        "prescriber_last_name",
        "prescriber_phone",
    )
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


class SentContactEmailInline(admin.TabularInline):
    model = SentContactEmail
    max_num = 0
    can_delete = False
    readonly_fields = ("date_sent", "recipient", "carbon_copies")


class LogItemInline(admin.TabularInline):
    model = LogItem
    max_num = 0
    can_delete = False
    fields = ("date", "message", "user")
    readonly_fields = ("date", "message", "user")


class OrientationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "beneficiary_last_name",
        "service",
        "creation_date",
        "prescriber_email",
        "processing_date",
        "status",
        "orientation_checked",
    )
    list_filter = (
        "status",
        "creation_date",
        "processing_date",
    )
    raw_id_fields = (
        "prescriber",
        "prescriber_structure",
        "service",
    )
    exclude = ("beneficiary_france_travail_number",)
    readonly_fields = (
        "service",
        "di_service_id",
        "di_service_name",
        "di_service_address_line",
        "di_contact_email",
        "di_contact_name",
        "di_contact_phone",
        "di_structure_name",
        "data_protection_commitment",
        "query_id",
        "query_expires_at",
        "original_service_name",
    )
    search_fields = (
        "beneficiary_last_name",
        "beneficiary_email",
        "referent_last_name",
        "referent_email",
        "original_service_name",
        "di_structure_name",
        "di_service_name",
    )
    date_hierarchy = "creation_date"
    ordering = ("-id",)
    filter_horizontal = ("rejection_reasons",)
    inlines = [EmploisOrientationDataInline, SentContactEmailInline, LogItemInline]

    @admin.display(description="e-mail prescripteur")
    def prescriber_email(self, obj) -> str:
        return obj.prescriber_info.email or "-"

    @admin.display(description="vérification")
    def orientation_checked(self, obj) -> bool:
        return not bool(check_orientation(obj))

    orientation_checked.boolean = True

    def get_object(self, request, obj_id, f):
        # quelques tests pour notifier d'avertissements concernant la demande l'orientation (ou pas)
        orientation = super().get_object(request, obj_id, f)

        if msgs := check_orientation(orientation):
            self.message_user(request, format_warnings(msgs), messages.WARNING)

        return orientation

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .prefetch_related(
                "prescriber_structure__membership",
                "service__structure__membership",
                "logitem_set",
            )
            .select_related(
                "prescriber",
                "prescriber_structure",
                "service",
                "service__structure",
                "emplois_orientation_data",
            )
        )
        return qs

    def get_fieldsets(self, request, obj=None):
        (_, opts) = super().get_fieldsets(request, obj)[0]
        fields = opts["fields"]
        other, di_fields = [], []
        for name in fields:
            if name.startswith("di_"):
                di_fields.append(name)
            else:
                other.append(name)
        out = []
        if other:
            out.append((None, {"fields": tuple(other)}))
        if di_fields:
            out.append(("D·I", {"fields": tuple(di_fields)}))
        return tuple(out)


admin.site.register(Orientation, OrientationAdmin)
