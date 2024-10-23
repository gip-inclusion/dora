from django.contrib import admin

from .models import Notification, NotificationLog


class NotificationLogInline(admin.TabularInline):
    model = NotificationLog
    fields = ("pk", "triggered_at", "status", "counter")
    readonly_fields = ("pk", "triggered_at", "counter", "status")
    extra = 0
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False


@admin.register(NotificationLog)
class NotificationLogsAdmin(admin.ModelAdmin):
    raw_id_fields = ("notification",)
    list_filter = ("task_type", "status")
    list_display = (
        "pk",
        "triggered_at",
        "task_type",
        "status",
        "counter",
    )
    readonly_fields = (
        "triggered_at",
        "notification",
        "owner",
        "task_type",
        "status",
        "counter",
    )
    search_fields = ("pk", "notification__id")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    raw_id_fields = ("owner_structure", "owner_user", "owner_structureputativemember")
    list_display = ("pk", "task_type", "created_at", "status")
    list_filter = ("task_type", "status")
    search_fields = (
        "pk",
        "owner_user__id",
        "owner_structure__id",
        "owner_structureputativemember__id",
    )
    inlines = (NotificationLogInline,)
