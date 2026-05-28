import uuid

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from dora.core.validators import validate_siret
from dora.orientations.models import EmploisOrientationData
from dora.orientations.serializers import OrientationSerializer
from dora.services.models import Service
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
    structure_siret = serializers.CharField(max_length=14, validators=[validate_siret])
    prescriber_id = serializers.UUIDField()
    prescriber_email = serializers.EmailField()
    prescriber_first_name = serializers.CharField(max_length=140)
    prescriber_last_name = serializers.CharField(max_length=140)
    prescriber_phone = serializers.CharField(max_length=10)


class EmploisOrientationSerializer(OrientationSerializer):
    """API Les Emplois : le service Dora est ciblé via `di_service_id` = `dora--` + UUID du service."""

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
            raise serializers.ValidationError(
                {
                    "data_protection_commitment": "Vous devez accepter l’engagement de protection des données."
                }
            )

        # Validation de l'identifiant de service DI
        di_service_id = attrs["di_service_id"]
        if "--" not in di_service_id:
            raise serializers.ValidationError(
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


class EmploisStatsSerializer(serializers.Serializer):
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
    service_id = serializers.CharField(allow_blank=True, required=False, default="")
    structure_id = serializers.CharField()
    source = serializers.CharField()
    external_link = serializers.URLField(
        allow_blank=True, required=False, allow_null=True, default=None
    )
    service_name = serializers.CharField(required=False, allow_blank=True, default="")
    structure_name = serializers.CharField(required=False, allow_blank=True, default="")
    structure_department = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=3
    )

    def validate_external_link(self, value):
        return value or None

    def validate(self, attrs):
        service_id = attrs.get("service_id")
        source = attrs["source"]

        if source == "dora":
            try:
                if service_id:
                    attrs["service"] = Service.objects.select_related(
                        "structure", "structure__source", "source"
                    ).get(pk=uuid.UUID(service_id.removeprefix("dora--").strip()))
                else:
                    attrs["structure"] = (
                        Structure.objects.select_related("source")
                        .only("pk", "department", "city_code", "source__value")
                        .get(
                            pk=uuid.UUID(
                                attrs["structure_id"].removeprefix("dora--").strip()
                            )
                        )
                    )
            except (ValueError, Service.DoesNotExist, Structure.DoesNotExist):
                if service_id:
                    raise NotFound("Service Dora introuvable pour cet identifiant.")
                raise NotFound("Structure Dora introuvable pour cet identifiant.")
        elif service_id:
            errors = {}
            for field in ("service_name", "structure_name", "structure_department"):
                if not attrs.get(field):
                    errors[field] = (
                        "Ce champ est obligatoire pour une mobilisation de service "
                        "hors Dora."
                    )
            if errors:
                raise serializers.ValidationError(errors)

        return attrs
