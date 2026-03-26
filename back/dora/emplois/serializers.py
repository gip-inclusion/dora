
from django.core.files.storage import default_storage
from django.db.models import Avg, DurationField, F
from django.db.models.expressions import ExpressionWrapper
from rest_framework import serializers

from dora.orientations.models import Orientation, OrientationStatus
from dora.services.models import Service
from dora.structures.models import DisabledDoraFormDIStructure

COACH_ORIENTATION_MODES_ORDER = {
    "formulaire-dora": 0,
    "envoyer-un-mail-avec-une-fiche-de-prescription": 1,
    "completer-le-formulaire-dadhesion": 2,
    "envoyer-un-mail": 3,
    "telephoner": 4,
    "autre": 5,
}

BENEFICIARIES_ACCESS_MODES_ORDER = {
    "se-presenter": 0,
    "completer-le-formulaire-dadhesion": 1,
    "envoyer-un-mail": 2,
    "telephoner": 3,
    "professionnel": 4,
    "autre": 5,
}


class ServiceSerializer(serializers.ModelSerializer):
    funding_labels = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="label"
    )
    forms_info = serializers.SerializerMethodField()
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
            "funding_labels",  # TODO: We need a reference API for the label
            "forms_info",  # TODO: Need `credentials` reference API
            "online_form",  # TODO: Need `credentials` reference API
            "credentials",  # TODO: We need a reference API for the label
            "is_orientable_with_form",
            "average_orientation_response_delay_days",
        ]

    def get_forms_info(self, obj):
        return [{"name": form, "url": default_storage.url(form)} for form in obj.forms]

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
