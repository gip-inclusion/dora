import logging
from datetime import timedelta

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.utils.timezone import now
from rest_framework import exceptions, serializers
from rest_framework.relations import PrimaryKeyRelatedField

import dora.data_inclusion.client
from dora.core.utils import code_insee_to_code_dept
from dora.services.enums import ServiceStatus
from dora.structures.models import Structure, StructureMember

from .models import (
    AccessCondition,
    AdminDivisionType,
    BeneficiaryAccessMode,
    Bookmark,
    CoachOrientationMode,
    Credential,
    FundingLabel,
    LocationKind,
    Public,
    Requirement,
    SavedSearch,
    Service,
    ServiceCategory,
    ServiceFee,
    ServiceKind,
    ServiceModel,
    ServiceSubCategory,
    UpdateFrequency,
)

logger = logging.getLogger(__name__)


class CreatablePrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.max_length = kwargs.pop("max_length", None)
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return True

    def to_internal_value(self, data):
        if isinstance(data, int):
            return super().to_internal_value(data)

        # If we receive a string instead of a primary key, search
        # by value, and create a new object if not found

        name = data.strip()
        if name == "":
            raise ValidationError("Cette valeur est vide")

        if self.max_length is not None and len(name) > self.max_length:
            raise ValidationError(
                f"Cette valeur doit avoir moins de {self.max_length} caractères"
            )

        if self.root.instance:
            structure = self.root.instance.structure
        else:
            structure_slug = self.root.initial_data["structure"]
            structure = Structure.objects.get(slug=structure_slug)
        if not structure:
            raise ValidationError("La structure ne peut pas être vide")
        queryset = self.queryset

        # find if it already exists in the same structure
        obj = queryset.filter(name=name, structure=structure).first()
        if not obj:
            # then in the global repository
            obj = queryset.filter(name=name, structure=None).first()
        if not obj:
            # otherwise create it
            obj = queryset.create(name=name, structure=structure)
        return obj


# On veut sérialiser le nom du champ pour les valeurs spécifiques à une
# structure, puisque l'utilisateur ne pourra pas la retrouver sur le frontend
# TODO: a simplifier: ça devrait devenir le mécanisme général, même pour
# sérialiser les services. Peut-être qu'on pourrait même toujours sérialiser directement
# les chaines au lieu des ids.
class ModelCreatablePrimaryKeyRelatedField(CreatablePrimaryKeyRelatedField):
    def to_representation(self, value):
        return value.name if value.structure else value.id


class StructureSerializer(serializers.ModelSerializer):
    has_admin = serializers.SerializerMethodField()
    num_services = serializers.SerializerMethodField()

    class Meta:
        model = Structure
        fields = [
            "address1",
            "address2",
            "city",
            "department",
            "has_admin",
            "name",
            "num_services",
            "postal_code",
            "short_desc",
            "siret",
            "slug",
            "url",
            "phone",
            "email",
        ]
        read_only_fields = [
            "city",
            "department",
        ]

    def get_has_admin(self, structure):
        return structure.has_admin()

    def get_num_services(self, structure):
        return structure.get_num_visible_services(self.context["request"].user)


def _get_diffusion_zone_type_display(obj):
    return (
        AdminDivisionType(obj.diffusion_zone_type).label
        if obj.diffusion_zone_type
        else ""
    )


def _get_update_frequency_display(obj):
    return UpdateFrequency(obj.update_frequency).label if obj.update_frequency else ""


class ServiceSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()
    forms_info = serializers.SerializerMethodField()
    structure = serializers.SlugRelatedField(
        queryset=Structure.objects.all(), slug_field="slug"
    )
    structure_info = StructureSerializer(source="structure", read_only=True)
    kinds = serializers.SlugRelatedField(
        slug_field="value",
        queryset=ServiceKind.objects.all(),
        many=True,
        required=False,
    )
    kinds_display = serializers.SlugRelatedField(
        source="kinds", slug_field="label", many=True, read_only=True
    )
    categories = serializers.SlugRelatedField(
        slug_field="value",
        queryset=ServiceCategory.objects.all(),
        many=True,
        required=False,
    )
    categories_display = serializers.SlugRelatedField(
        source="categories", slug_field="label", many=True, read_only=True
    )
    subcategories = serializers.SlugRelatedField(
        slug_field="value",
        queryset=ServiceSubCategory.objects.all(),
        many=True,
        required=False,
    )
    subcategories_display = serializers.SlugRelatedField(
        source="subcategories", slug_field="label", many=True, read_only=True
    )
    funding_labels = serializers.SlugRelatedField(
        slug_field="value",
        queryset=FundingLabel.objects.all(),
        many=True,
        required=False,
    )
    funding_labels_display = serializers.SlugRelatedField(
        source="funding_labels", slug_field="label", many=True, read_only=True
    )
    access_conditions = CreatablePrimaryKeyRelatedField(
        many=True,
        queryset=AccessCondition.objects.all(),
        max_length=140,
        required=False,
    )
    access_conditions_display = serializers.SerializerMethodField()
    publics = CreatablePrimaryKeyRelatedField(
        many=True,
        queryset=Public.objects.all(),
        max_length=140,
        required=False,
    )
    publics_display = serializers.SerializerMethodField()
    requirements = CreatablePrimaryKeyRelatedField(
        many=True,
        queryset=Requirement.objects.all(),
        max_length=140,
        required=False,
    )
    requirements_display = serializers.SerializerMethodField()
    credentials = CreatablePrimaryKeyRelatedField(
        many=True,
        queryset=Credential.objects.all(),
        max_length=140,
        required=False,
    )
    credentials_display = serializers.SerializerMethodField()
    location_kinds = serializers.SlugRelatedField(
        slug_field="value",
        queryset=LocationKind.objects.all(),
        many=True,
        required=False,
    )
    location_kinds_display = serializers.SlugRelatedField(
        source="location_kinds", slug_field="label", many=True, read_only=True
    )
    diffusion_zone_type_display = serializers.SerializerMethodField()
    diffusion_zone_details_display = serializers.SerializerMethodField()
    beneficiaries_access_modes = serializers.SlugRelatedField(
        slug_field="value",
        queryset=BeneficiaryAccessMode.objects.all(),
        many=True,
        required=False,
    )
    beneficiaries_access_modes_display = serializers.SlugRelatedField(
        source="beneficiaries_access_modes",
        slug_field="label",
        many=True,
        read_only=True,
    )
    coach_orientation_modes = serializers.SlugRelatedField(
        slug_field="value",
        queryset=CoachOrientationMode.objects.all(),
        many=True,
        required=False,
    )
    coach_orientation_modes_display = serializers.SlugRelatedField(
        source="coach_orientation_modes", slug_field="label", many=True, read_only=True
    )
    department = serializers.SerializerMethodField()
    can_write = serializers.SerializerMethodField()
    has_already_been_unpublished = serializers.SerializerMethodField()

    model_changed = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()
    model = serializers.SlugRelatedField(
        queryset=ServiceModel.objects.all(),
        slug_field="slug",
        required=False,
        allow_null=True,
    )

    fee_condition = serializers.SlugRelatedField(
        queryset=ServiceFee.objects.all(),
        slug_field="value",
        required=False,
        allow_null=True,
    )

    update_frequency_display = serializers.SerializerMethodField()

    update_needed = serializers.SerializerMethodField()

    is_orientable_ft_service = serializers.SerializerMethodField()

    class Meta:
        model = Service

        fields = [
            "access_conditions",
            "access_conditions_display",
            "address1",
            "address2",
            "address_line",
            "beneficiaries_access_modes",
            "beneficiaries_access_modes_display",
            "beneficiaries_access_modes_external_form_link",
            "beneficiaries_access_modes_external_form_link_text",
            "beneficiaries_access_modes_other",
            "can_write",
            "categories",
            "categories_display",
            "city",
            "city_code",
            "coach_orientation_modes",
            "coach_orientation_modes_display",
            "coach_orientation_modes_external_form_link",
            "coach_orientation_modes_external_form_link_text",
            "coach_orientation_modes_other",
            "publics",
            "publics_display",
            "contact_info_filled",
            "contact_email",
            "contact_name",
            "contact_phone",
            "creation_date",
            "credentials",
            "credentials_display",
            "department",
            "diffusion_zone_details",
            "diffusion_zone_details_display",
            "diffusion_zone_type",
            "diffusion_zone_type_display",
            "duration_weekly_hours",
            "duration_weeks",
            "fee_condition",
            "fee_details",
            "forms",
            "forms_info",
            "full_desc",
            "funding_labels",
            "funding_labels_display",
            "geom",
            "has_already_been_unpublished",
            "is_available",
            "is_contact_info_public",
            "is_cumulative",
            "is_model",
            "is_orientable",
            "kinds",
            "kinds_display",
            "location_kinds",
            "location_kinds_display",
            "model",
            "model_changed",
            "model_name",
            "modification_date",
            "name",
            "online_form",
            "postal_code",
            "publication_date",
            "qpv_or_zrr",
            "recurrence",
            "remote_url",
            "requirements",
            "requirements_display",
            "short_desc",
            "slug",
            "status",
            "structure",
            "structure",
            "structure_info",
            "subcategories",
            "subcategories_display",
            "suspension_date",
            "update_frequency",
            "update_frequency_display",
            "update_needed",
            "use_inclusion_numerique_scheme",
            "is_orientable_ft_service",
        ]
        read_only_fields = [
            "city",
            "is_model",
        ]
        lookup_field = "slug"

    def get_category(self, obj):
        # On n'utilise volontairement pas .first() ici pour éviter une requete supplémentaire
        # (obj.categories est caché via un prefetch_related)
        cats = obj.categories.all()
        return cats[0].value if cats else ""

    def get_category_display(self, obj):
        # On n'utilise volontairement pas .first() ici pour éviter une requete supplémentaire
        # (obj.categories est caché via un prefetch_related)
        cats = obj.categories.all()
        return cats[0].label if cats else ""

    def get_is_available(self, obj):
        return True

    def get_has_already_been_unpublished(self, obj):
        # Note : on ne peut pas se baser sur le `new_status` car les services
        # fraîchement publiés ne deviendront plus éligibles au formulaire Tally...
        return obj.status_history_item.filter(
            previous_status=ServiceStatus.PUBLISHED
        ).exists()

    def get_forms_info(self, obj):
        forms = [{"name": form, "url": default_storage.url(form)} for form in obj.forms]
        return forms

    def get_diffusion_zone_type_display(self, obj):
        return _get_diffusion_zone_type_display(obj)

    def get_diffusion_zone_details_display(self, obj):
        return obj.get_diffusion_zone_details_display()

    def get_access_conditions_display(self, obj):
        return [item.name for item in obj.access_conditions.all()]

    def get_publics_display(self, obj):
        return [item.name for item in obj.publics.all()]

    def get_requirements_display(self, obj):
        return [item.name for item in obj.requirements.all()]

    def get_credentials_display(self, obj):
        return [item.name for item in obj.credentials.all()]

    def get_department(self, obj):
        code = obj.city_code
        return code_insee_to_code_dept(code)

    def get_can_write(self, obj):
        user = self.context.get("request").user
        return obj.can_write(user)

    def validate(self, data):
        user = self.context.get("request").user
        structure = data.get("structure") or self.instance.structure

        if structure.no_dora_form() and "coach_orientation_modes" in data:
            data["coach_orientation_modes"] = [
                mode
                for mode in data["coach_orientation_modes"]
                if mode.value != "formulaire-dora"
            ]

        user_structures = StructureMember.objects.filter(user_id=user.id).values_list(
            "structure_id", flat=True
        )

        if "structure" in data:
            if not data["structure"].can_edit_services(user):
                raise exceptions.PermissionDenied()

        if "access_conditions" in data:
            self._validate_custom_choice(
                "access_conditions", data, user, user_structures, structure
            )

        if "publics" in data:
            self._validate_custom_choice(
                "publics", data, user, user_structures, structure
            )

        if "requirements" in data:
            self._validate_custom_choice(
                "requirements", data, user, user_structures, structure
            )

        if "credentials" in data:
            self._validate_custom_choice(
                "credentials", data, user, user_structures, structure
            )

        return data

    def _validate_custom_choice(self, field, data, user, user_structures, structure):
        values = data[field]
        for val in values:
            if val.structure_id is not None and val.structure_id != structure.id:
                raise serializers.ValidationError(
                    {field: "Ce choix n'est pas disponible dans cette structure"},
                    "unallowed_custom_choices_bad_struc",
                )

        return values

    def get_model_changed(self, object):
        if object.model:
            return object.model.sync_checksum != object.last_sync_checksum
        return None

    def get_model_name(self, object):
        if object.model:
            return object.model.name
        return None

    def get_update_frequency_display(self, obj):
        return _get_update_frequency_display(obj)

    def get_update_needed(self, object):
        return object.get_update_needed()

    def get_is_orientable_ft_service(self, obj):
        return obj.is_orientable_ft_service()


class ServiceModelSerializer(ServiceSerializer):
    num_services = serializers.SerializerMethodField()
    access_conditions = ModelCreatablePrimaryKeyRelatedField(
        many=True,
        queryset=AccessCondition.objects.all(),
        max_length=140,
        required=False,
    )

    publics = ModelCreatablePrimaryKeyRelatedField(
        many=True,
        queryset=Public.objects.all(),
        max_length=140,
        required=False,
    )
    requirements = ModelCreatablePrimaryKeyRelatedField(
        many=True,
        queryset=Requirement.objects.all(),
        max_length=140,
        required=False,
    )
    credentials = ModelCreatablePrimaryKeyRelatedField(
        many=True,
        queryset=Credential.objects.all(),
        max_length=140,
        required=False,
    )
    funding_labels = serializers.SlugRelatedField(
        slug_field="value",
        queryset=FundingLabel.objects.all(),
        many=True,
        required=False,
    )
    funding_labels_display = serializers.SlugRelatedField(
        source="funding_labels", slug_field="label", many=True, read_only=True
    )

    class Meta:
        model = ServiceModel

        fields = [
            "access_conditions",
            "access_conditions_display",
            "beneficiaries_access_modes",
            "beneficiaries_access_modes_display",
            "beneficiaries_access_modes_external_form_link",
            "beneficiaries_access_modes_external_form_link_text",
            "beneficiaries_access_modes_other",
            "can_write",
            "categories",
            "categories_display",
            "coach_orientation_modes",
            "coach_orientation_modes_display",
            "coach_orientation_modes_external_form_link",
            "coach_orientation_modes_external_form_link_text",
            "coach_orientation_modes_other",
            "publics",
            "publics_display",
            "creation_date",
            "credentials",
            "credentials_display",
            "department",
            "duration_weekly_hours",
            "duration_weeks",
            "fee_condition",
            "fee_details",
            "forms",
            "forms_info",
            "funding_labels",
            "funding_labels_display",
            "full_desc",
            "is_cumulative",
            "is_model",
            "kinds",
            "kinds_display",
            "modification_date",
            "name",
            "num_services",
            "online_form",
            "qpv_or_zrr",
            "recurrence",
            "requirements",
            "requirements_display",
            "short_desc",
            "slug",
            "structure",
            "structure_info",
            "subcategories",
            "subcategories_display",
            "suspension_date",
            "update_frequency",
        ]
        read_only_fields = [
            "is_model",
        ]
        lookup_field = "slug"

    def get_num_services(self, obj):
        return obj.copies.exclude(status=ServiceStatus.ARCHIVED).count()


class AnonymousServiceSerializer(ServiceSerializer):
    contact_name = serializers.SerializerMethodField()
    contact_phone = serializers.SerializerMethodField()
    contact_email = serializers.SerializerMethodField()
    is_contact_info_public = serializers.SerializerMethodField()

    def get_contact_name(self, obj):
        return obj.contact_name if obj.is_contact_info_public else ""

    def get_contact_phone(self, obj):
        return obj.contact_phone if obj.is_contact_info_public else ""

    def get_contact_email(self, obj):
        return obj.contact_email if obj.is_contact_info_public else ""

    def get_is_contact_info_public(self, obj):
        return True if obj.is_contact_info_public else None


class StructureSerializerInList(StructureSerializer):
    class Meta:
        model = Structure
        fields = [
            "address1",
            "address2",
            "city",
            "department",
            "name",
            "postal_code",
            "short_desc",
            "siret",
            "slug",
            "url",
        ]
        read_only_fields = ["city", "department"]


class ServiceListSerializer(ServiceSerializer):
    structure_info = StructureSerializerInList(source="structure", read_only=True)

    diffusion_zone_type_display = serializers.SerializerMethodField()
    diffusion_zone_details_display = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "categories_display",
            "city",
            "coach_orientation_modes",
            "contact_email",
            "contact_name",
            "contact_phone",
            "department",
            "diffusion_zone_details_display",
            "diffusion_zone_type",
            "diffusion_zone_type_display",
            "model",
            "model_changed",
            "modification_date",
            "name",
            "postal_code",
            "short_desc",
            "slug",
            "status",
            "structure",
            "structure_info",
            "use_inclusion_numerique_scheme",
        ]
        read_only_fields = [
            "city",
        ]
        lookup_field = "slug"

    def get_diffusion_zone_type_display(self, obj):
        return _get_diffusion_zone_type_display(obj)

    def get_diffusion_zone_details_display(self, obj):
        return obj.get_diffusion_zone_details_display()


class FeedbackSerializer(serializers.Serializer):
    reasons = serializers.ListField(child=serializers.CharField())
    notify_support = serializers.BooleanField(required=False, default=False)
    name = serializers.CharField()
    email = serializers.EmailField()
    details = serializers.CharField()


class SavedSearchSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        with_counts = kwargs.pop("with_new_services_count", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if not with_counts:
            self.fields.pop("new_services_count")

    category = serializers.SlugRelatedField(
        slug_field="value",
        queryset=ServiceCategory.objects.all(),
        required=False,
    )
    category_display = serializers.SlugRelatedField(
        source="category", slug_field="label", read_only=True
    )

    subcategories = serializers.SlugRelatedField(
        slug_field="value",
        queryset=ServiceSubCategory.objects.all(),
        many=True,
        required=False,
    )
    subcategories_display = serializers.SlugRelatedField(
        source="subcategories", slug_field="label", many=True, read_only=True
    )

    kinds = serializers.SlugRelatedField(
        slug_field="value",
        queryset=ServiceKind.objects.all(),
        many=True,
        required=False,
    )
    kinds_display = serializers.SlugRelatedField(
        source="kinds", slug_field="label", many=True, read_only=True
    )

    fees = serializers.SlugRelatedField(
        slug_field="value",
        queryset=ServiceFee.objects.all(),
        many=True,
        required=False,
    )
    fees_display = serializers.SlugRelatedField(
        source="fees", slug_field="label", many=True, read_only=True
    )
    location_kinds = serializers.SlugRelatedField(
        slug_field="value",
        queryset=LocationKind.objects.all(),
        many=True,
        required=False,
    )
    location_kinds_display = serializers.SlugRelatedField(
        source="location_kinds", slug_field="label", many=True, read_only=True
    )
    funding_labels = serializers.SlugRelatedField(
        slug_field="value",
        queryset=FundingLabel.objects.all(),
        many=True,
        required=False,
    )
    funding_labels_display = serializers.SlugRelatedField(
        source="funding_labels", slug_field="label", many=True, read_only=True
    )

    new_services_count = serializers.SerializerMethodField()

    class Meta:
        model = SavedSearch
        fields = [
            "id",
            "category",
            "category_display",
            "city_code",
            "city_label",
            "creation_date",
            "fees",
            "fees_display",
            "frequency",
            "subcategories",
            "subcategories_display",
            "kinds",
            "kinds_display",
            "location_kinds",
            "location_kinds_display",
            "funding_labels",
            "funding_labels_display",
            "new_services_count",
        ]

    def get_new_services_count(self, obj):
        return len(
            obj.get_recent_services(
                (now() - timedelta(days=settings.RECENT_SERVICES_CUTOFF_DAYS)).date()
            )
        )


class BookmarkListSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    is_di = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ["id", "slug", "is_di", "creation_date"]

    def get_slug(self, obj):
        if obj.service_id:
            return obj.service.slug
        else:
            return obj.di_id

    def get_is_di(self, obj):
        return True if obj.di_id else False


class BookmarkSerializer(BookmarkListSerializer):
    service = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = [
            "id",
            "slug",
            "is_di",
            "creation_date",
            "service",
        ]

    def get_service(self, obj):
        service = obj.service
        if service:
            return {
                "structure_slug": obj.service.structure.slug,
                "structure_name": obj.service.structure.name,
                "postal_code": obj.service.postal_code,
                "city": obj.service.city,
                "name": obj.service.name,
                "shortDesc": obj.service.short_desc,
                # ServiceSource n'est pas sérialisable en JSON
                "source": str(obj.service.source),
            }
        else:
            # note : pour pouvoir être mocké correctement,
            # le client D·I doit être importé avec le *même* chemin que
            # celui utilisé au moment du `patch`
            # (sinon, le mock échoue)
            di_client = dora.data_inclusion.di_client_factory()

            try:
                di_service = (
                    di_client.retrieve_service(id=obj.di_id)
                    if di_client is not None
                    else None
                )
            except requests.ConnectionError:
                return {}
            if di_service is None:
                return {}
            return {
                "structure_name": di_service["structure"]["nom"],
                "postal_code": di_service["code_postal"],
                "city": di_service["commune"],
                "name": di_service["nom"],
                "shortDesc": di_service["presentation_resume"] or "",
                "source": di_service["source"],
            }


class SearchResultSerializer(ServiceListSerializer):
    distance = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "address1",
            "address2",
            "beneficiaries_access_modes",
            "city",
            "coach_orientation_modes",
            "coordinates",
            "diffusion_zone_type",
            "distance",
            "fee_condition",
            "funding_labels",
            "kinds",
            "location_kinds",
            "modification_date",
            "name",
            "postal_code",
            "publication_date",
            "short_desc",
            "slug",
            "status",
            "structure",
            "structure_info",
        ]

    def get_distance(self, obj):
        return obj.distance.km if obj.distance is not None else None

    def get_coordinates(self, obj):
        if obj.geom:
            return (obj.geom.x, obj.geom.y)


class FundingLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingLabel
        fields = [
            "value",
            "label",
        ]
