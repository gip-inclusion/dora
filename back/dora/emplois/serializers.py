import itertools

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
    diffusion_zone = serializers.CharField(
        source="get_diffusion_zone_details_display", read_only=True
    )
    publics = serializers.SerializerMethodField()
    eligibility_requirements = serializers.SerializerMethodField()
    funding_labels = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="label"
    )
    mobilization_modes_professionals = serializers.SerializerMethodField()
    mobilization_modes_individuals = serializers.SerializerMethodField()
    forms_info = serializers.SerializerMethodField()
    credentials = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    kinds = serializers.SlugRelatedField(many=True, read_only=True, slug_field="label")
    is_orientable_with_dora_form = serializers.SerializerMethodField()
    average_orientation_response_delay_days = serializers.SerializerMethodField()

    class Meta:
        model = Service

        fields = [
            "id",
            "diffusion_zone",
            "short_desc",
            "publics",
            "eligibility_requirements",
            "is_cumulative",
            "funding_labels",
            "mobilization_modes_professionals",
            "mobilization_modes_individuals",
            "forms_info",
            "online_form",
            "credentials",
            "kinds",
            "is_orientable_with_dora_form",
            "is_contact_info_public",
            "average_orientation_response_delay_days",
        ]

    def get_publics(self, obj):
        publics = list(obj.publics.all())
        if not publics:
            return ["Tous publics"]
        return [p.name for p in publics]

    def get_eligibility_requirements(self, obj):
        eligibility_requirements = list(
            itertools.chain(
                (ac.name for ac in obj.access_conditions.all()),
                (r.name for r in obj.requirements.all()),
            )
        )
        if obj.qpv_or_zrr:
            eligibility_requirements.append("Uniquement QPV ou ZFRR")
        return eligibility_requirements

    def get_mobilization_modes_professionals(self, obj):
        modes = sorted(
            obj.coach_orientation_modes.all(),
            key=lambda m: COACH_ORIENTATION_MODES_ORDER.get(m.value, 999),
        )
        result = []
        for m in modes:
            if m.value == "formulaire-dora":
                name = "Orienter votre bénéficiaire via le formulaire DORA"
            elif (
                m.value == "envoyer-un-mail-avec-une-fiche-de-prescription"
                and obj.contact_email
            ):
                name = "Envoyer un email avec une fiche de prescription"
            elif m.value == "autre":
                name = obj.coach_orientation_modes_other
            else:
                name = m.label

            result.append(
                {
                    "name": name,
                    "link": (
                        obj.coach_orientation_modes_external_form_link
                        if m.value == "completer-le-formulaire-dadhesion"
                        and obj.coach_orientation_modes_external_form_link
                        else None
                    ),
                    "custom": m.value == "autre",
                }
            )

        return result

    def get_mobilization_modes_individuals(self, obj):
        modes = sorted(
            obj.beneficiaries_access_modes.all(),
            key=lambda m: BENEFICIARIES_ACCESS_MODES_ORDER.get(m.value, 999),
        )
        result = []
        for m in modes:
            if m.value == "completer-le-formulaire-dadhesion":
                name = (
                    obj.beneficiaries_access_modes_external_form_link_text
                    or "Faire une demande"
                )
            elif m.value == "professionnel":
                name = "Orientation par un professionnel"
            elif m.value == "autre":
                name = obj.beneficiaries_access_modes_other
            else:
                name = m.label

            result.append(
                {
                    "name": name,
                    "link": (
                        obj.beneficiaries_access_modes_external_form_link
                        if m.value == "completer-le-formulaire-dadhesion"
                        and obj.beneficiaries_access_modes_external_form_link
                        else None
                    ),
                    "custom": m.value == "autre",
                }
            )

        return result

    def get_forms_info(self, obj):
        return [{"name": form, "url": default_storage.url(form)} for form in obj.forms]

    def get_is_orientable_with_dora_form(self, obj):
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
