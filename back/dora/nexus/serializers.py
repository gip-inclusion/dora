from itoutils.django.nexus.token import decode_token
from rest_framework import serializers


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
