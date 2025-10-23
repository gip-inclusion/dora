from rest_framework import serializers

from dora.users.models import ConsentRecord


class ConsentRecordSerializer(serializers.ModelSerializer):
    consent_choices = serializers.DictField(child=serializers.BooleanField())

    anonymous_user_hash = serializers.CharField(
        min_length=32,
        max_length=32,
    )

    class Meta:
        model = ConsentRecord
        fields = ["anonymous_user_hash", "consent_version", "consent_choices"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None

        if user:
            validated_data["user"] = user

        return super().create(validated_data)
