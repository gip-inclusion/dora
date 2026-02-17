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
