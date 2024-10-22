from django.core.files.storage import default_storage
from rest_framework import serializers

from dora.orientations.models import Orientation
from dora.services.models import Service
from dora.structures.models import Structure


class OrientationSerializer(serializers.ModelSerializer):
    service_slug = serializers.SlugRelatedField(
        source="service",
        slug_field="slug",
        queryset=Service.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    prescriber_structure_slug = serializers.SlugRelatedField(
        source="prescriber_structure",
        slug_field="slug",
        queryset=Structure.objects.all(),
        write_only=True,
    )

    # TODO: utiliser un vrai champ pour stocker l'état initial
    # TODO: est-ce qu'il faut la même chose pour la structure?
    service = serializers.SerializerMethodField()
    prescriber_structure = serializers.SerializerMethodField()
    prescriber = serializers.SerializerMethodField()
    beneficiary_attachments_details = serializers.SerializerMethodField()

    class Meta:
        model = Orientation
        fields = [
            "beneficiary_attachments",
            "beneficiary_attachments_details",
            "beneficiary_availability",
            "beneficiary_contact_preferences",
            "beneficiary_email",
            "beneficiary_first_name",
            "beneficiary_last_name",
            "beneficiary_other_contact_method",
            "beneficiary_phone",
            "creation_date",
            "di_service_id",
            "di_service_name",
            "di_contact_email",
            "di_contact_name",
            "di_contact_phone",
            "di_structure_name",
            "id",
            "orientation_reasons",
            "prescriber",
            "prescriber_structure",
            "prescriber_structure_slug",
            "processing_date",
            "query_id",
            "referent_email",
            "referent_first_name",
            "referent_last_name",
            "referent_phone",
            "requirements",
            "service",
            "service_slug",
            "situation",
            "situation_other",
            "status",
        ]
        extra_kwargs = {"beneficiary_attachments": {"write_only": True}}

    def get_service(self, orientation):
        return {
            "contact_email": orientation.get_contact_email(),
            "contact_name": orientation.get_contact_name(),
            "contact_phone": orientation.get_contact_phone(),
            "structure_name": orientation.get_structure_name(),
            "name": orientation.get_service_name(),
            "slug": orientation.service.slug
            if orientation.service
            else f"di--{orientation.di_service_id}",
            "is_di": bool(orientation.di_service_id),
        }

    def get_prescriber_structure(self, orientation):
        return {
            "name": orientation.prescriber_structure.name
            if orientation.prescriber_structure
            else "",
            "slug": orientation.prescriber_structure.slug
            if orientation.prescriber_structure
            else "",
        }

    def get_prescriber(self, orientation):
        return {
            "name": orientation.prescriber.get_full_name(),
            "email": orientation.prescriber.email,
        }

    def get_beneficiary_attachments_details(self, orientation):
        return [
            {"name": a, "url": default_storage.url(a)}
            for a in orientation.beneficiary_attachments
        ]
