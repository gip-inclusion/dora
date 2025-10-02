from rest_framework import serializers

from dora.core.models import LogItem, ModerationStatus
from dora.services.models import Service, ServiceModel
from dora.services.serializers import ServiceSerializer
from dora.structures.models import Structure, StructureMember, StructurePutativeMember
from dora.structures.serializers import StructureSerializer
from dora.users.models import User


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "date_joined",
            "email",
            "email",
            "first_name",
            "is_active",
            "is_valid",
            "last_name",
            "newsletter",
        ]
        read_only_fields = [
            "date_joined",
            "email",
            "email",
            "first_name",
            "is_active",
            "is_valid",
            "last_name",
            "newsletter",
        ]


class LogItemSerializer(serializers.ModelSerializer):
    user = UserAdminSerializer()

    class Meta:
        fields = ["user", "message", "date"]
        model = LogItem


class StructureAdminSerializer(StructureSerializer):
    branches = serializers.SerializerMethodField()
    creator = UserAdminSerializer()
    last_editor = UserAdminSerializer()
    members = serializers.SerializerMethodField()
    models = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()
    pending_members = serializers.SerializerMethodField()
    services = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

    # TdB
    categories = serializers.SerializerMethodField()
    has_admin = serializers.SerializerMethodField()
    num_services = serializers.SerializerMethodField()
    num_draft_services = serializers.SerializerMethodField()
    num_published_services = serializers.SerializerMethodField()
    num_outdated_services = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()
    editors = serializers.SerializerMethodField()
    admins_to_moderate = serializers.SerializerMethodField()
    admins_to_remind = serializers.SerializerMethodField()
    num_potential_members_to_validate = serializers.SerializerMethodField()
    num_potential_members_to_remind = serializers.SerializerMethodField()
    is_orphan = serializers.SerializerMethodField()
    is_waiting = serializers.SerializerMethodField()
    awaiting_moderation = serializers.SerializerMethodField()
    awaiting_activation = serializers.SerializerMethodField()
    awaiting_update = serializers.SerializerMethodField()

    class Meta:
        model = Structure
        fields = [
            "address1",
            "address2",
            "admins",
            "admins_to_moderate",
            "admins_to_remind",
            "ape",
            "awaiting_moderation",
            "awaiting_activation",
            "awaiting_update",
            "branches",
            "categories",
            "city",
            "creation_date",
            "creator",
            "department",
            "editors",
            "email",
            "full_desc",
            "has_admin",
            "is_orphan",
            "is_waiting",
            "last_editor",
            "latitude",
            "longitude",
            "members",
            "models",
            "moderation_date",
            "moderation_status",
            "modification_date",
            "name",
            "notes",
            "num_draft_services",
            "num_outdated_services",
            "num_potential_members_to_remind",
            "num_potential_members_to_validate",
            "num_published_services",
            "num_services",
            "parent",
            "pending_members",
            "phone",
            "postal_code",
            "services",
            "short_desc",
            "siret",
            "slug",
            "source",
            "typology",
            "typology_display",
            "url",
        ]
        read_only_fields = [
            "address1",
            "address2",
            "admins",
            "admins_to_moderate",
            "admins_to_remind",
            "ape",
            "awaiting_moderation",
            "awaiting_activation",
            "awaiting_update",
            "branches",
            "categories",
            "city",
            "creation_date",
            "creator",
            "department",
            "editors",
            "email",
            "full_desc",
            "has_admin",
            "is_orphan",
            "is_waiting",
            "last_editor",
            "latitude",
            "longitude",
            "members",
            "models",
            "moderation_date",
            "modification_date",
            "name",
            "notes",
            "num_draft_services",
            "num_outdated_services",
            "num_potential_members_to_remind",
            "num_potential_members_to_validate",
            "num_published_services",
            "num_services",
            "parent",
            "pending_members",
            "phone",
            "postal_code",
            "services",
            "short_desc",
            "siret",
            "slug",
            "source",
            "typology",
            "typology_display",
            "url",
        ]
        lookup_field = "slug"

    def get_members(self, obj):
        class SMSerializer(serializers.ModelSerializer):
            user = UserAdminSerializer()

            class Meta:
                model = StructureMember
                fields = ["user", "is_admin", "creation_date"]

        return SMSerializer(obj.membership, many=True).data

    def get_pending_members(self, obj):
        class SPMSerializer(serializers.ModelSerializer):
            user = UserAdminSerializer()

            class Meta:
                model = StructurePutativeMember
                fields = ["user", "is_admin", "creation_date", "invited_by_admin"]

        return SPMSerializer(obj.putative_membership, many=True).data

    def get_source(self, obj):
        return obj.source.label if obj.source else ""

    def get_parent(self, obj):
        if obj.parent:
            return {
                "name": obj.parent.name,
                "slug": obj.parent.slug,
            }
        return {}

    def get_branches(self, obj):
        class BranchSerializer(serializers.ModelSerializer):
            class Meta:
                model = Structure
                fields = ["slug", "name", "short_desc"]
                lookup_field = "slug"

        return BranchSerializer(obj.branches.all(), many=True).data

    def get_models(self, obj):
        models = ServiceModel.objects.filter(structure=obj)

        class ModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = ServiceModel
                fields = ["slug", "name", "short_desc"]
                lookup_field = "slug"

        return ModelSerializer(models, many=True).data

    def get_services(self, obj):
        class ServiceSerializer(serializers.ModelSerializer):
            class Meta:
                model = Service
                fields = ["slug", "name", "short_desc"]
                lookup_field = "slug"

        return ServiceSerializer(obj.services.published(), many=True).data

    def get_notes(self, obj):
        logs = LogItem.objects.filter(structure=obj).order_by("-date")
        return LogItemSerializer(logs, many=True).data

    def get_has_admin(self, obj):
        return getattr(obj, "has_valid_admin", False)

    def get_num_draft_services(self, obj):
        return getattr(obj, "num_draft_services", 0)

    def get_num_published_services(self, obj):
        return getattr(obj, "num_published_services", 0)

    def get_num_outdated_services(self, obj):
        return getattr(obj, "num_outdated_services", 0)

    def get_num_services(self, obj):
        return getattr(obj, "num_active_services", 0)

    def get_categories(self, obj):
        categories = getattr(obj, "categories_list", None)
        return [c for c in categories if c is not None] if categories else []

    def get_admins(self, obj):
        emails = getattr(obj, "admin_emails", None)
        return [e for e in emails if e is not None] if emails else []

    def get_editors(self, obj):
        emails = getattr(obj, "editor_emails", None)
        return list(set(e for e in emails if e is not None)) if emails else []

    def get_admins_to_moderate(self, obj):
        if obj.moderation_status != ModerationStatus.VALIDATED:
            return self.get_admins(obj)
        return []

    def get_admins_to_remind(self, obj):
        if not getattr(obj, "has_valid_admin", False):
            return [
                member.user.email
                for member in getattr(obj, "potential_members", [])
                if member.is_admin and member.invited_by_admin
            ]
        return []

    def get_num_potential_members_to_validate(self, obj):
        potential_members_to_validate = [
            member
            for member in getattr(obj, "potential_members", [])
            if member.user.is_valid and not member.invited_by_admin
        ]

        return len(potential_members_to_validate)

    def get_num_potential_members_to_remind(self, obj):
        potential_members_to_validate = [
            member
            for member in getattr(obj, "potential_members", [])
            if member.invited_by_admin
        ]

        return len(potential_members_to_validate)

    def get_is_orphan(self, obj):
        return getattr(obj, "is_orphan", False)

    def get_is_waiting(self, obj):
        return len(self.get_admins_to_remind(obj)) > 0

    def get_awaiting_moderation(self, obj):
        return getattr(obj, "awaiting_moderation", False)

    def get_awaiting_activation(self, obj):
        return self.get_num_published_services(obj) == 0

    def get_awaiting_update(self, obj):
        return bool(getattr(obj, "num_outdated_services", None))


class StructureAdminListSerializer(StructureAdminSerializer):
    class Meta:
        model = Structure
        fields = [
            "admins",
            "admins_to_moderate",
            "admins_to_remind",
            "awaiting_moderation",
            "awaiting_activation",
            "awaiting_update",
            "categories",
            "city",
            "department",
            "editors",
            "email",
            "has_admin",
            "is_obsolete",
            "is_orphan",
            "is_waiting",
            "latitude",
            "longitude",
            "moderation_date",
            "moderation_status",
            "name",
            "national_labels",
            "num_draft_services",
            "num_outdated_services",
            "num_potential_members_to_remind",
            "num_potential_members_to_validate",
            "num_published_services",
            "num_services",
            "phone",
            "short_desc",
            "siret",
            "slug",
            "typology",
            "typology_display",
        ]
        read_only_fields = [
            "admins",
            "admins_to_moderate",
            "admins_to_remind",
            "awaiting_moderation",
            "awaiting_activation",
            "awaiting_update",
            "categories",
            "city",
            "department",
            "editors",
            "email",
            "has_admin",
            "is_obsolete",
            "is_orphan",
            "is_waiting",
            "latitude",
            "longitude",
            "moderation_date",
            "name",
            "national_labels",
            "num_draft_services",
            "num_outdated_services",
            "num_potential_members_to_remind",
            "num_potential_members_to_validate",
            "num_published_services",
            "num_services",
            "phone",
            "short_desc",
            "siret",
            "slug",
            "typology",
            "typology_display",
        ]
        lookup_field = "slug"


class ServiceAdminSerializer(ServiceSerializer):
    creator = UserAdminSerializer()
    last_editor = UserAdminSerializer()
    model = serializers.SerializerMethodField()
    structure = StructureAdminSerializer()
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "categories_display",
            "city",
            "contact_email",
            "contact_name",
            "contact_phone",
            "creation_date",
            "creator",
            "department",
            "diffusion_zone_details_display",
            "diffusion_zone_type_display",
            "fee_condition",
            "fee_details",
            "full_desc",
            "is_contact_info_public",
            "last_editor",
            "model",
            "moderation_date",
            "moderation_status",
            "modification_date",
            "name",
            "notes",
            "postal_code",
            "short_desc",
            "slug",
            "structure",
            "subcategories_display",
        ]
        read_only_fields = [
            "categories_display",
            "city",
            "contact_email",
            "contact_name",
            "contact_phone",
            "creation_date",
            "creator",
            "department",
            "diffusion_zone_details_display",
            "diffusion_zone_type_display",
            "fee_condition",
            "fee_details",
            "full_desc",
            "is_contact_info_public",
            "last_editor",
            "model",
            "moderation_date",
            "modification_date",
            "name",
            "notes",
            "postal_code",
            "short_desc",
            "slug",
            "structure",
            "subcategories_display",
        ]
        lookup_field = "slug"

    def get_model(self, obj):
        if obj.model:
            return {"name": obj.model.name, "slug": obj.model.slug}
        return {}

    def get_notes(self, obj):
        logs = LogItem.objects.filter(service=obj).order_by("-date")
        return LogItemSerializer(logs, many=True).data


class ServiceAdminListSerializer(ServiceAdminSerializer):
    structure_name = serializers.SerializerMethodField()
    structure_dept = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "diffusion_zone_details_display",
            "diffusion_zone_type",
            "diffusion_zone_type_display",
            "moderation_date",
            "moderation_status",
            "name",
            "slug",
            "structure_dept",
            "structure_name",
        ]
        read_only_fields = [
            "diffusion_zone_details_display",
            "diffusion_zone_type",
            "diffusion_zone_type_display",
            "name",
            "slug",
            "structure_dept",
            "structure_name",
        ]

    def get_structure_name(self, obj):
        return obj.structure.name

    def get_structure_dept(self, obj):
        return obj.structure.department
