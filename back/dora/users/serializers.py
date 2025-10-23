from rest_framework import serializers

from dora.users.models import ConsentRecord


class ConsentRecordSerializer(serializers.ModelSerializer):
    consent_choices = serializers.DictField(child=serializers.BooleanField())

    class Meta:
        model = ConsentRecord
        fields = ["anonymous_user_hash", "consent_version", "consent_choices"]

    def validate(self, data):
        data = super().validate(data)

        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None
        anonymous_user_hash = data.get("anonymous_user_hash")

        if not user and not anonymous_user_hash:
            raise serializers.ValidationError(
                "Doit fournir anonymous_user_hash ou être connecté"
            )

        return data

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None

        if user:
            validated_data["user"] = user
            validated_data["anonymous_user_hash"] = None

        return super().create(validated_data)
