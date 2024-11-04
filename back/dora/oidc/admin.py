from django.contrib import admin

from .models import UserSession


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "session")
    readonly_fields = ("user", "session")
    list_display = ("pk", "user", "session")
    search_fields = ("pk", "user__email", "session__pk", "user__pk")
