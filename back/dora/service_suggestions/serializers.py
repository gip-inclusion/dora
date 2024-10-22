import logging

from django.db.transaction import rollback, set_autocommit
from rest_framework import serializers
from sentry_sdk import capture_exception

from dora.services.serializers import ServiceSerializer
from dora.users.models import User

from .models import ServiceSuggestion

logger = logging.getLogger(__name__)


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["get_full_name", "email"]


class ServiceSuggestionSerializer(serializers.ModelSerializer):
    structure_info = serializers.SerializerMethodField()
    service_info = serializers.SerializerMethodField()
    creator = CreatorSerializer(read_only=True)

    class Meta:
        model = ServiceSuggestion
        extra_kwargs = {"contents": {"write_only": True}}

        fields = [
            "contents",
            "creator",
            "id",
            "name",
            "service_info",
            "siret",
            "structure_info",
        ]

    def get_structure_info(self, suggestion):
        return suggestion.get_structure_info()

    def get_service_info(self, suggestion):
        # Crée un service fictif, immédiatement suivi d'un rollback
        set_autocommit(False)
        try:
            service, _ = suggestion.convert_to_service()
            result = ServiceSerializer(
                service, context={"request": self.context.get("request")}
            ).data
        except Exception as e:
            capture_exception(e)
            result = {}
        rollback()
        set_autocommit(True)
        return result
