from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dora.service_suggestions.models import ServiceSuggestion

from .serializers import ServiceSuggestionSerializer


class ServiceSuggestionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Anybody can create a new contribution
        if request.method == "POST":
            return True
        else:
            # Only staff can do anything else
            return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_staff


class ServiceSuggestionValidationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class ServiceSuggestionViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [ServiceSuggestionPermission]
    serializer_class = ServiceSuggestionSerializer

    def get_queryset(self):
        return ServiceSuggestion.objects.all().order_by("-creation_date")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(
            creator=user,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="validate",
        permission_classes=[ServiceSuggestionValidationPermission],
    )
    def validate_suggestion(self, request, pk):
        suggestion = self.get_object()
        _, emails_contacted = suggestion.convert_to_service(
            send_notification_mail=True, user=request.user
        )

        return Response({"emails_contacted": emails_contacted}, status=201)
