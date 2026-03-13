import itertools

from django.core.files.storage import default_storage
from rest_framework import serializers

from dora.services.models import Service

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
    id = serializers.SerializerMethodField()
    diffusion_zone = serializers.SerializerMethodField()
    short_desc = serializers.CharField(read_only=True)
    publics = serializers.SerializerMethodField()
    eligibility_requirements = serializers.SerializerMethodField()
    is_cumulative = serializers.BooleanField(read_only=True)
    funding_labels = serializers.SerializerMethodField()
    mobilization_modes_professionals = serializers.SerializerMethodField()
    mobilization_modes_individuals = serializers.SerializerMethodField()
    forms_info = serializers.SerializerMethodField()
    online_form = serializers.SerializerMethodField()
    credentials = serializers.SerializerMethodField()
    kinds = serializers.SerializerMethodField()
    is_orientable_with_dora_form = serializers.SerializerMethodField()
    is_contact_info_public = serializers.BooleanField(read_only=True)

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
        ]

    def get_id(self, obj):
        return str(obj.id)

    def get_diffusion_zone(self, obj):
        return obj.get_diffusion_zone_details_display()

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

    def get_funding_labels(self, obj):
        return [label.label for label in obj.funding_labels.all()]

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

    def get_online_form(self, obj):
        return obj.online_form or None

    def get_credentials(self, obj):
        return [c.name for c in obj.credentials.all()]

    def get_kinds(self, obj):
        return [k.label for k in obj.kinds.all()]

    def get_is_orientable_with_dora_form(self, obj):
        return obj.is_orientable() and any(
            mode.value == "formulaire-dora"
            for mode in obj.coach_orientation_modes.all()
        )
