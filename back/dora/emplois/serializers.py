from django.db.models import Avg, DurationField, F
from django.db.models.expressions import ExpressionWrapper
from rest_framework import serializers

from dora.orientations.models import Orientation, OrientationStatus
from dora.services.models import Service
from dora.structures.models import DisabledDoraFormDIStructure


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
        prefetched = getattr(obj, "_prefetched_objects_cache", {}).get("orientations")
        if prefetched is not None:
            delays = [(o.processing_date - o.creation_date).days for o in prefetched]
            return round(sum(delays) / len(delays)) if delays else None
        result = (
            Orientation.objects.filter(
                service=obj,
                status__in=[
                    OrientationStatus.ACCEPTED,
                    OrientationStatus.REJECTED,
                ],
                processing_date__isnull=False,
            )
            .annotate(
                delay=ExpressionWrapper(
                    F("processing_date") - F("creation_date"),
                    output_field=DurationField(),
                ),
            )
            .aggregate(avg_delay=Avg("delay"))
        )
        avg_delay = result["avg_delay"]
        if avg_delay is None:
            return None
        return round(avg_delay.total_seconds() / 86400)


class DisabledDoraFormDIStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabledDoraFormDIStructure
        fields = ["source", "structure_id"]
