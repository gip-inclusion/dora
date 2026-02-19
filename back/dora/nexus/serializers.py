from itoutils.django.nexus.token import decode_token
from rest_framework import serializers

from dora.nexus.constants import NEXUS_MENU_ENABLED_DEPARTMENTS
from dora.structures.models import StructureMember


class NexusMenuStatusSerializer(serializers.Serializer):
    proconnect = serializers.BooleanField()
    activated_services = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
    )
    enabled = serializers.SerializerMethodField()

    def get_enabled(self, obj):
        if not obj.get("mvp-enabled", False):
            return False

        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        return StructureMember.objects.filter(
            user=request.user,
            structure__department__in=NEXUS_MENU_ENABLED_DEPARTMENTS,
        ).exists()


class OrientationBeneficiaryInfoInputSerializer(serializers.Serializer):
    jwt = serializers.CharField(required=True)

    def validate_jwt(self, value):
        try:
            claims = decode_token(value)
        except ValueError:
            raise serializers.ValidationError("Token JWT invalide.")

        if "beneficiary" not in claims:
            raise serializers.ValidationError("Données bénéficiaire absentes du token.")

        return claims


class OrientationBeneficiaryInfoOutputSerializer(serializers.Serializer):
    uid = serializers.CharField(default="")
    first_name = serializers.CharField(default="")
    last_name = serializers.CharField(default="")
    email = serializers.CharField(default="")
    phone = serializers.CharField(default="")
    france_travail_id = serializers.CharField(default="")
