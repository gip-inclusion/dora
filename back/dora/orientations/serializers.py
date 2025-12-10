import requests
from django.core.files.storage import default_storage
from rest_framework import serializers

import dora.data_inclusion.client
from dora.orientations.models import Orientation, OrientationStatus
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

    def validate(self, orientation):
        """Valide l'engagement de protection des données et les documents joints.

        L'engagement de protection des données (`data_protection_commitment`) doit être True lors de la création.

        Si au moins un document (`Service.forms`) ou justificatif (`Service.credentials`) est demandé par le service,
        alors le bénéficiaire doit joindre au moins un document (`Orientation.beneficiary_attachments`).
        S'il n'y en a pas, une erreur est levée.

        À la fois les services Dora et DI sont supportés.
        """
        # Validation de l'engagement de protection des données
        if not self.instance and not orientation.get("data_protection_commitment"):
            raise serializers.ValidationError(
                {
                    "data_protection_commitment": "Vous devez accepter l’engagement de protection des données."
                }
            )

        # Récupère le service depuis les données ou l'instance
        service = orientation.get("service") or (
            self.instance.service if self.instance else None
        )

        if service:
            # Il s'agit d'un service Dora

            # Est-ce que le service nécessite des documents ou justificatifs ?
            requires_attachments = (
                service.credentials.exists()  # A des justificatifs requis
                or bool(service.forms)  # A des documents à compléter
            )
        elif orientation.get("di_service_id"):
            # Il s'agit d'un service DI

            # Récupération du service depuis le client DI
            di_client = dora.data_inclusion.di_client_factory()
            try:
                raw_service = (
                    di_client.retrieve_service(id=orientation.get("di_service_id"))
                    if di_client is not None
                    else None
                )
            except requests.ConnectionError:
                return orientation
            if raw_service is None:
                return orientation

            # Mapping du service DI
            di_service = dora.data_inclusion.map_service(raw_service, False)

            # Est-ce que le service DI nécessite des documents ou justificatifs ?
            requires_attachments = (
                bool(di_service.get("credentials"))  # A des justificatifs requis
                or bool(di_service.get("forms"))  # A des documents à compléter
            )

        # Si le service nécessite des documents mais qu'aucun n'est fourni, une erreur est levée.
        if requires_attachments and not orientation.get("beneficiary_attachments"):
            raise serializers.ValidationError(
                {
                    "beneficiary_attachments": "Pour valider l’envoi de votre demande, vous devez ajouter les documents demandés."
                }
            )

        return orientation

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
        return (
            obj.prescriber.get_full_name() if obj.prescriber else "Utilisateur supprimé"
        )

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
        ]

    @staticmethod
    def get_prescriber_structure_name(obj: Orientation) -> str:
        return (
            obj.prescriber_structure.name
            if obj.prescriber_structure
            else "Pas de prescripteur"
        )

    @staticmethod
    def get_detail_page_url(obj: Orientation) -> str:
        return obj.get_magic_link()
