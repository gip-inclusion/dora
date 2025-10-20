from django.contrib import admin

from .models import ConsentRecord, ImportJob, LogItem


class EnumAdmin(admin.ModelAdmin):
    list_display = [
        "value",
        "label",
    ]
    search_fields = (
        "value",
        "label",
    )
    ordering = ["label"]


class LogItemAdmin(admin.ModelAdmin):
    list_display = ["service", "structure", "user", "message"]
    readonly_fields = ["date"]
    raw_id_fields = ["structure", "service", "user"]


class ImportJobAdmin(admin.ModelAdmin):
    list_display = [
        "filename",
        "import_type",
        "user",
        "status",
        "created_at",
        "completed_at",
    ]
    list_filter = ["status", "import_type", "created_at"]
    search_fields = ["filename", "user__email", "user__first_name", "user__last_name"]
    readonly_fields = [
        "id",
        "user",
        "import_type",
        "filename",
        "status",
        "created_at",
        "started_at",
        "completed_at",
    ]
    raw_id_fields = ["user"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ConsentRecordAdmin(admin.ModelAdmin):
    list_display = [
        "get_user_identifier",
        "consent_version",
        "consented_to_google",
        "consented_to_matomo",
        "created_at",
    ]

    list_filter = [
        "consent_version",
        "consented_to_google",
        "consented_to_matomo",
        "created_at",
    ]

    search_fields = [
        "user__email",
        "user__username",
        "anonymous_id",
        "id",
    ]

    ordering = ["-created_at"]

    readonly_fields = [
        "id",
        "user",
        "anonymous_id",
        "consent_version",
        "consented_to_google",
        "consented_to_matomo",
        "created_at",
    ]

    fieldsets = (
        ("Identification", {"fields": ("id", "user", "anonymous_id")}),
        (
            "Consentement",
            {
                "fields": (
                    "consent_version",
                    "consented_to_google",
                    "consented_to_matomo",
                )
            },
        ),
        ("Métadonnées", {"fields": ("created_at",)}),
    )

    @admin.display(description="Identifiant", ordering="user__email")
    def get_user_identifier(self, obj):
        if obj.user:
            return obj.user.email
        return f"Anonyme ({obj.anonymous_id[:8]})" if obj.anonymous_id else "N/A"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(LogItem, LogItemAdmin)
admin.site.register(ImportJob, ImportJobAdmin)
admin.site.register(ConsentRecord, ConsentRecordAdmin)
