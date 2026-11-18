from django.core.files.storage import default_storage
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import serializers

from dora.orientations.models import (
    EMPLOIS_SOURCE_LABEL,
    Orientation,
    OrientationStatus,
)


class OrientationSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    prescriber_structure = serializers.SerializerMethodField()
    prescriber = serializers.SerializerMethodField()
    beneficiary_attachments_details = serializers.SerializerMethodField()

    class Meta:
        model = Orientation
        fields = [
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
            "id",
            "orientation_reasons",
            "prescriber",
            "prescriber_structure",
            "processing_date",
            "query_id",
            "referent_email",
            "referent_first_name",
            "referent_last_name",
            "referent_phone",
            "requirements",
            "service",
            "situation",
            "situation_other",
            "source",
            "status",
        ]

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
        prescriber = orientation.prescriber_info
        return {
            "name": prescriber.structure_name,
            "slug": prescriber.structure_slug,
            "url": prescriber.structure_url or None,
        }

    def get_prescriber(self, orientation):
        prescriber = orientation.prescriber_info
        return {"name": prescriber.full_name, "email": prescriber.email}

    def get_beneficiary_attachments_details(self, orientation):
        return [
            {"name": a, "url": default_storage.url(a)}
            for a in orientation.beneficiary_attachments
        ]

    def to_representation(self, instance):
        """Contrôle la représentation des champs en lecture."""
        data = super().to_representation(instance)

        # Le numéro France Travail n'est retourné que si l'orientation est validée
        if instance.status != "VALIDÉE":
            data["beneficiary_france_travail_number"] = ""

        return data


class SentOrientationExportSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%d")
    beneficiary_name = serializers.SerializerMethodField()
    prescriber_name = serializers.SerializerMethodField()
    structure_name = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    @staticmethod
    def get_beneficiary_name(obj: Orientation) -> str:
        return obj.get_beneficiary_full_name()

    @staticmethod
    def get_prescriber_name(obj: Orientation) -> str:
        return obj.prescriber_info.full_name or "Utilisateur supprimé"

    @staticmethod
    def get_structure_name(obj: Orientation) -> str:
        return obj.get_structure_name()

    @staticmethod
    def get_service_name(obj: Orientation) -> str:
        return obj.get_service_name()

    @staticmethod
    def get_status(obj: Orientation) -> str:
        return OrientationStatus(obj.status).label

    class Meta:
        model = Orientation
        fields = [
            "creation_date",
            "status",
            "beneficiary_name",
            "prescriber_name",
            "structure_name",
            "service_name",
        ]


class ReceivedOrientationExportSerializer(SentOrientationExportSerializer):
    prescriber_structure_name = serializers.SerializerMethodField()
    detail_page_url = serializers.SerializerMethodField()
    beneficiary_france_travail_number = serializers.SerializerMethodField()

    class Meta:
        model = Orientation
        fields = [
            "creation_date",
            "status",
            "beneficiary_name",
            "prescriber_name",
            "service_name",
            "prescriber_structure_name",
            "detail_page_url",
            "source",
            "beneficiary_france_travail_number",
        ]

    @staticmethod
    def get_prescriber_structure_name(obj: Orientation) -> str:
        return obj.prescriber_info.structure_name or "Pas de prescripteur"

    @staticmethod
    def get_detail_page_url(obj: Orientation) -> str:
        return obj.get_magic_link()

    @staticmethod
    def get_beneficiary_france_travail_number(obj: Orientation) -> str:
        if obj.status == OrientationStatus.ACCEPTED:
            return obj.beneficiary_france_travail_number
        return ""


class EmploisReceivedOrientationExportSerializer(serializers.Serializer):
    """La sortie des orientations reçues depuis l'API des Emplois de l'inclusion
    est la même que ReceivedOrientationExportSerializer afin que les deux jeux de données
    puissent être concaténés dans un même export.
    """

    creation_date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    beneficiary_name = serializers.SerializerMethodField()
    prescriber_name = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()
    prescriber_structure_name = serializers.SerializerMethodField()
    detail_page_url = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField()
    beneficiary_france_travail_number = serializers.SerializerMethodField()

    @staticmethod
    def get_creation_date(obj: dict) -> str:
        created_at = parse_datetime(obj.get("created_at") or "")
        if created_at is None:
            return ""
        if timezone.is_aware(created_at):
            created_at = timezone.localtime(created_at)
        return created_at.strftime("%Y-%m-%d")

    @staticmethod
    def get_status(obj: dict) -> str:
        try:
            return OrientationStatus(obj.get("status")).label
        except ValueError:
            return obj.get("status") or ""

    @staticmethod
    def get_beneficiary_name(obj: dict) -> str:
        return obj.get("beneficiary_name") or ""

    @staticmethod
    def get_prescriber_name(obj: dict) -> str:
        return obj.get("sender_name") or ""

    def get_service_name(self, obj: dict) -> str:
        service_names = self.context.get("service_names", {})
        return service_names.get(obj.get("service_uid"), "")

    @staticmethod
    def get_prescriber_structure_name(obj: dict) -> str:
        return obj.get("sender_organization_name") or ""

    @staticmethod
    def get_detail_page_url(obj: dict) -> str:
        return obj.get("process_link") or ""

    @staticmethod
    def get_source(obj: dict) -> str:
        return EMPLOIS_SOURCE_LABEL

    @staticmethod
    def get_beneficiary_france_travail_number(obj: dict) -> str:
        # Même règle que pour les orientations Dora : le numéro n'est exposé
        # que sur les orientations validées.
        if obj.get("status") == OrientationStatus.ACCEPTED:
            return obj.get("france_travail_id") or ""
        return ""
