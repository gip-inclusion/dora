from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from dora.services.models import Bookmark, SavedSearch
from dora.structures.models import StructureMember, StructurePutativeMember

from .models import ConsentRecord, User


class StructureMemberInline(admin.TabularInline):
    model = StructureMember
    readonly_fields = ["structure"]
    extra = 0

    def has_add_permission(self, request, obj):
        return False


class StructurePutativeMemberInline(admin.TabularInline):
    model = StructurePutativeMember
    readonly_fields = ["structure"]
    extra = 0

    def has_add_permission(self, request, obj):
        return False


class SavedSearchInline(admin.TabularInline):
    model = SavedSearch
    fields = ["city_code", "city_label", "category", "creation_date"]
    readonly_fields = ["city_code", "city_label", "category", "creation_date"]
    extra = 0
    ordering = ["-creation_date"]

    def has_add_permission(self, request, obj):
        return False


class BookmarkInline(admin.TabularInline):
    model = Bookmark
    readonly_fields = ["service", "creation_date"]
    extra = 0
    ordering = ["-creation_date"]

    def has_add_permission(self, request, obj):
        return False


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "email",
        "get_full_name",
        "is_staff",
        "is_manager",
        "is_active",
        "is_valid",
        "date_joined",
        "main_activity",
    )
    list_filter = (
        "is_staff",
        "is_manager",
        "is_active",
        "is_valid",
        "departments",
        "main_activity",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "last_name",
                    "first_name",
                    "main_activity",
                    "discovery_method",
                    "discovery_method_other",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_manager",
                    "departments",
                    "is_active",
                    "is_valid",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "last_name", "first_name")
    readonly_fields = ["discovery_method", "discovery_method_other"]
    ordering = ("-date_joined",)
    filter_horizontal = ()
    inlines = [
        StructureMemberInline,
        StructurePutativeMemberInline,
        SavedSearchInline,
        BookmarkInline,
    ]


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

    list_select_related = ["user"]

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

        return mark_safe(html)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(ConsentRecord, ConsentRecordAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
