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
        "get_consents_display",
        "created_at",
    ]

    list_filter = [
        "consent_version",
        "created_at",
    ]

    search_fields = [
        "user__email",
        "anonymous_id",
        "id",
    ]

    ordering = ["-created_at"]

    readonly_fields = [
        "id",
        "user",
        "anonymous_id",
        "consent_version",
        "get_consents_formatted",
        "created_at",
    ]

    fieldsets = (
        ("Identification", {"fields": ("id", "user", "anonymous_id")}),
        ("Consentement", {"fields": ("consent_version", "get_consents_formatted")}),
        ("Métadonnées", {"fields": ("created_at",)}),
    )

    # Méthode pour afficher l'identifiant utilisateur
    @admin.display(description="Identifiant", ordering="user__email")
    def get_user_identifier(self, obj):
        if obj.user:
            return obj.user.email
        return f"Anonyme ({obj.anonymous_id[:8]}...)" if obj.anonymous_id else "N/A"

    # Méthode pour afficher les consentements dans la liste (compact)
    @admin.display(description="Consentements")
    def get_consents_display(self, obj):
        if not obj.consent_choices:
            return "Aucun"

        # Créer une liste des services acceptés
        accepted = [
            key.replace("_", " ").title()
            for key, value in obj.consent_choices.items()
            if value is True
        ]

        if not accepted:
            return "❌ Tous refusés"

        return "✓ " + ", ".join(accepted)

    @admin.display(description="Consentements par service")
    def get_consents_formatted(self, obj):
        if not obj.consent_choices:
            return "Aucun consentement enregistré"

        from django.utils.html import format_html

        rows = []
        for service, consented in obj.consent_choices.items():
            icon = "✓" if consented else "✗"
            color = "#28a745" if consented else "#dc3545"
            service_name = service.replace("_", " ").title()
            rows.append(
                f"<tr>"
                f'<td style="padding: 8px; font-weight: bold;">{service_name}</td>'
                f'<td style="padding: 8px; color: {color}; font-size: 16px;">{icon}</td>'
                f'<td style="padding: 8px;">{"Accepté" if consented else "Refusé"}</td>'
                f"</tr>"
            )

        html = f"""
        <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
            <thead>
                <tr style="background-color: #f8f9fa;">
                    <th style="padding: 8px; text-align: left; border-bottom: 2px solid #dee2e6;">Service</th>
                    <th style="padding: 8px; text-align: center; border-bottom: 2px solid #dee2e6;">Statut</th>
                    <th style="padding: 8px; text-align: left; border-bottom: 2px solid #dee2e6;">Décision</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
        """

        return format_html(html)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(LogItem, LogItemAdmin)
admin.site.register(ImportJob, ImportJobAdmin)
admin.site.register(ConsentRecord, ConsentRecordAdmin)
