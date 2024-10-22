from rest_framework import permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["main_activity", "discovery_method", "discovery_method_other"]

    def validate(self, attrs):
        if "main_activity" not in attrs and not self.instance.main_activity:
            raise serializers.ValidationError(
                "Le champ « Activité principale » est requis"
            )
        return attrs


@api_view(["PATCH", "POST"])  # TODO: remove POST when not used by frontend anymore
@permission_classes([permissions.IsAuthenticated])
def update_user_profile(request):
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=204)
