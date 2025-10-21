from rest_framework import serializers

from dora.core.models import ConsentRecord


class ConsentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentRecord
        fields = ["anonymous_id", "consent_version", "consent_choices"]

    def validate_consent_choices(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Le consentement doit être dans un objet JSON"
            )

        for key, val in value.items():
            if not isinstance(val, bool):
                raise serializers.ValidationError(
                    f"La valeur pour '{key}' doit être un booléen (true/false)"
                )

        return value

    def validate(self, data):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None
        anonymous_id = data.get("anonymous_id")

        if not user and not anonymous_id:
            raise serializers.ValidationError(
                "Doit fournir anonymous_id ou être connecté"
            )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None

        if user:
            validated_data["user"] = user
            validated_data["anonymous_id"] = None

        return super().create(validated_data)
