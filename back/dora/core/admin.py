from django.contrib import admin

from .models import ImportJob, LogItem


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
    list_display = ["date", "message", "user", "service", "structure", "orientation"]
    readonly_fields = ["date", "message", "user", "service", "structure", "orientation"]


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


admin.site.register(LogItem, LogItemAdmin)
admin.site.register(ImportJob, ImportJobAdmin)
