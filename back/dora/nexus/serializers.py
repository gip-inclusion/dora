from rest_framework import serializers


class DropdownStatusSerializer(serializers.Serializer):
    proconnect = serializers.BooleanField()
    activated_services = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
    )
    mvp_enabled = serializers.BooleanField(source="mvp-enabled")
