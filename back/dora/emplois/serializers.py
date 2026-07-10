import uuid

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from dora.core.validators import validate_siret
from dora.orientations.models import EmploisOrientationData
from dora.orientations.serializers import OrientationSerializer
from dora.services.models import Service
from dora.stats.models import (
    DiMobilisationEvent,
    MobilisationEvent,
    StructureInfosView,
)
from dora.structures.models import DisabledDoraFormDIStructure, Structure


class ReferenceDataSerializer(serializers.Serializer):
    kind = serializers.CharField()
    label = serializers.CharField()
    value = serializers.CharField()


class ServiceSerializer(serializers.ModelSerializer):
    funding_labels = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="value"
    )
    coach_orientation_modes = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="value"
    )
    beneficiaries_access_modes = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="value"
    )
    forms = serializers.ListField(child=serializers.CharField())
    access_conditions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    credentials = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    is_orientable_with_form = serializers.SerializerMethodField()
    average_orientation_response_delay_days = serializers.SerializerMethodField()

    class Meta:
        model = Service

        fields = [
            "id",
            "short_desc",
            "recurrence",
            "funding_labels",
            "coach_orientation_modes",
            "coach_orientation_modes_other",
            "coach_orientation_modes_external_form_link",
            "coach_orientation_modes_external_form_link_text",
            "beneficiaries_access_modes",
            "beneficiaries_access_modes_other",
            "beneficiaries_access_modes_external_form_link",
            "beneficiaries_access_modes_external_form_link_text",
            "forms",
            "online_form",
            "access_conditions",
            "credentials",
            "is_orientable_with_form",
            "contact_name",
            "contact_phone",
            "contact_email",
            "is_contact_info_public",
            "average_orientation_response_delay_days",
        ]

    def get_is_orientable_with_form(self, obj):
        return obj.is_orientable() and any(
            mode.value == "formulaire-dora"
            for mode in obj.coach_orientation_modes.all()
        )

    def get_average_orientation_response_delay_days(self, obj):
        """Délai moyen de réponse aux demandes d'orientation, en jours."""
        orientations = obj.answered_orientations
        delays = [(o.processing_date - o.creation_date).days for o in orientations]
        if not delays:
            return None
        return round(sum(delays) / len(delays))


class DisabledDoraFormDIStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabledDoraFormDIStructure
        fields = ["source", "structure_id"]


class EmploisOrientationDataSerializer(serializers.Serializer):
    """Sérialiseur pour les données d'orientation complémentaires des Emplois."""

    beneficiary_id = serializers.UUIDField()
    structure_id = serializers.UUIDField()
    structure_name = serializers.CharField(max_length=140)
    structure_siret = serializers.CharField(
        max_length=14, validators=[validate_siret], required=False, allow_blank=True
    )
    prescriber_id = serializers.UUIDField()
    prescriber_email = serializers.EmailField()
    prescriber_first_name = serializers.CharField(max_length=140)
    prescriber_last_name = serializers.CharField(max_length=140)
    prescriber_phone = serializers.CharField(max_length=10)


class EmploisOrientationCreateSerializer(OrientationSerializer):
    """Création d'une orientation par Les Emplois : le service Dora est ciblé via `di_service_id` = `dora--` + UUID du service."""

    emplois_data = EmploisOrientationDataSerializer(write_only=True)

    class Meta(OrientationSerializer.Meta):
        fields = [
            "beneficiary_attachments",
            "beneficiary_attachments_details",
            "beneficiary_availability",
            "beneficiary_contact_preferences",
            "beneficiary_email",
            "beneficiary_france_travail_number",
            "beneficiary_first_name",
            "beneficiary_last_name",
            "beneficiary_other_contact_method",
            "beneficiary_phone",
            "creation_date",
            "data_protection_commitment",
            "di_service_id",
            "di_service_name",
            "di_service_address_line",
            "di_contact_email",
            "di_contact_name",
            "di_contact_phone",
            "di_structure_name",
            "emplois_data",
            "orientation_reasons",
            "referent_email",
            "referent_first_name",
            "referent_last_name",
            "referent_phone",
            "requirements",
            "service",
            "situation",
            "situation_other",
        ]
        extra_kwargs = {
            "beneficiary_attachments": {"write_only": True},
            "di_service_id": {
                "required": True,
                "allow_blank": False,
                "error_messages": {
                    "required": (
                        "L'identifiant de service est obligatoire (format « source--id »)."
                    ),
                    "blank": (
                        "L'identifiant de service est obligatoire (format « source--id »)."
                    ),
                },
            },
        }

    def validate_beneficiary_attachments(self, value):
        raise serializers.ValidationError(
            "Ce champ est renseigné à partir des fichiers joints "
            "et ne peut pas être fourni directement."
        )

    def create(self, validated_data):
        emplois_data = validated_data.pop("emplois_data")
        with transaction.atomic():
            orientation = super().create(validated_data)
            EmploisOrientationData.objects.create(
                orientation=orientation, **emplois_data
            )
        return orientation

    def validate(self, attrs):
        # Validation de l'engagement de protection des données
        if not self.instance and not attrs.get("data_protection_commitment"):
            raise ValidationError(
                {
                    "data_protection_commitment": "Vous devez accepter l’engagement de protection des données."
                }
            )

        # Validation de l'identifiant de service DI
        di_service_id = attrs["di_service_id"]
        if "--" not in di_service_id:
            raise ValidationError(
                {
                    "di_service_id": "Format d'identifiant invalide (attendu : « source--id »)."
                }
            )
        if di_service_id.startswith("dora--"):
            suffix = di_service_id.removeprefix("dora--").strip()
            try:
                service_pk = uuid.UUID(suffix)
                service = Service.objects.get(pk=service_pk)
            except (ValueError, Service.DoesNotExist):
                raise NotFound("Service Dora introuvable pour cet identifiant.")
            attrs["service"] = service
            attrs["di_service_id"] = ""
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.service_id:
            data["di_service_id"] = f"dora--{instance.service_id}"
        return data


# Valeurs constantes communes à tous les événements de mobilisation enregistrés
# via l'API des Emplois : il n'y a jamais d'utilisateur authentifié côté Dora.
_EVENT_DEFAULTS = {
    "path": "",
    "user": None,
    "is_logged": False,
    "is_staff": False,
    "is_manager": False,
    "is_an_admin": False,
}


class BaseMobilisationSerializer(serializers.ModelSerializer):
    """Champs communs à tous les événements de mobilisation des Emplois."""

    anonymous_user_hash = serializers.RegexField(
        r"^[0-9a-f]{32}$",
        error_messages={
            "invalid": "Doit contenir exactement 32 caractères hexadécimaux."
        },
    )
    user_kind = serializers.RegexField(
        r"^emplois_.+",
        error_messages={"invalid": "Doit commencer par « emplois_ »."},
    )

    def validate_external_link(self, value):
        return value or None


class DoraServiceMobilisationSerializer(BaseMobilisationSerializer):
    """Mobilisation d'un service Dora → MobilisationEvent."""

    service_id = serializers.CharField()

    class Meta:
        model = MobilisationEvent
        fields = ["anonymous_user_hash", "user_kind", "service_id", "external_link"]

    def validate(self, attrs):
        try:
            pk = uuid.UUID(attrs.pop("service_id").removeprefix("dora--").strip())
            attrs["service"] = Service.objects.select_related(
                "structure", "structure__source", "source"
            ).get(pk=pk)
        except (ValueError, Service.DoesNotExist):
            raise NotFound("Service Dora introuvable pour cet identifiant.")
        return attrs

    def create(self, validated_data):
        service = validated_data.pop("service")
        structure = service.structure
        return MobilisationEvent.objects.create(
            **_EVENT_DEFAULTS,
            **validated_data,
            service=service,
            structure=structure,
            is_structure_member=False,
            is_structure_admin=False,
            structure_department=structure.department,
            structure_city_code=structure.city_code,
            structure_source=structure.source.value if structure.source else "",
            service_source=service.source.value if service.source else "",
            update_needed=service.get_update_needed(),
            status=service.status,
        )


class DoraStructureViewSerializer(BaseMobilisationSerializer):
    """Consultation des informations d'une structure Dora → StructureInfosView."""

    structure_id = serializers.CharField()

    class Meta:
        model = StructureInfosView
        fields = ["anonymous_user_hash", "user_kind", "structure_id"]

    def validate(self, attrs):
        try:
            pk = uuid.UUID(attrs.pop("structure_id").removeprefix("dora--").strip())
            attrs["structure"] = (
                Structure.objects.select_related("source")
                .only("pk", "department", "city_code", "source__value")
                .get(pk=pk)
            )
        except (ValueError, Structure.DoesNotExist):
            raise NotFound("Structure Dora introuvable pour cet identifiant.")
        return attrs

    def create(self, validated_data):
        structure = validated_data.pop("structure")
        return StructureInfosView.objects.create(
            **_EVENT_DEFAULTS,
            **validated_data,
            structure=structure,
            is_structure_member=False,
            is_structure_admin=False,
            structure_department=structure.department,
            structure_city_code=structure.city_code,
            structure_source=structure.source.value if structure.source else "",
        )


class ExternalServiceMobilisationSerializer(BaseMobilisationSerializer):
    """Mobilisation d'un service hors Dora → DiMobilisationEvent."""

    structure_department = serializers.CharField(max_length=3)

    class Meta:
        model = DiMobilisationEvent
        fields = [
            "anonymous_user_hash",
            "user_kind",
            "service_id",
            "structure_id",
            "source",
            "service_name",
            "structure_name",
            "structure_department",
            "external_link",
        ]
        extra_kwargs = {
            "service_id": {"required": True, "allow_blank": False},
            "structure_id": {"required": True, "allow_blank": False},
            "service_name": {"required": True, "allow_blank": False},
            "structure_name": {"required": True, "allow_blank": False},
        }

    def create(self, validated_data):
        return DiMobilisationEvent.objects.create(
            **_EVENT_DEFAULTS,
            **validated_data,
        )
