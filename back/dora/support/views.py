from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.pagination import OptionalPageNumberPagination
from dora.core.utils import TRUTHY_VALUES
from dora.services.enums import ServiceStatus
from dora.services.models import Service
from dora.structures.models import Structure
from dora.support.serializers import (
    ServiceAdminListSerializer,
    ServiceAdminSerializer,
    StructureAdminListOptimizedSerializer,
    StructureAdminSerializer,
)


class StructureAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in [*permissions.SAFE_METHODS, "PATCH"]:
            return (
                user
                and user.is_authenticated
                and (user.is_staff or (user.is_manager and user.departments))
            )
        return False


class ServiceAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in [*permissions.SAFE_METHODS, "PATCH"]:
            return user and user.is_authenticated and user.is_staff
        return False


class ModerationMixin:
    def perform_update(self, serializer):
        status_before_update = serializer.instance.moderation_status
        status_after_update = (
            ModerationStatus(serializer.validated_data.get("moderation_status"))
            or status_before_update
        )

        if not status_before_update != status_after_update:
            raise serializers.ValidationError(
                "Mise à jour du statut de modération sans changement de statut"
            )
        msg = "Statut de modération changé par un•e membre de l'équipe"
        send_moderation_notification(
            serializer.instance, self.request.user, msg, status_after_update
        )


class StructureAdminViewSet(
    ModerationMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StructureAdminSerializer
    permission_classes = [StructureAdminPermission]
    pagination_class = OptionalPageNumberPagination

    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        department = self.request.query_params.get("department")

        # Queryset simplifié pour éviter les annotations coûteuses
        structures = (
            Structure.objects.all()
            .select_related("parent", "creator", "last_editor", "source")
            .prefetch_related(
                "membership__user",
                "putative_membership__user",
                "services__categories",
                "branches",
                "services",
                "services__model",
                "logitem_set",
            )
            # Supprimer toutes les annotations coûteuses
            # Elles seront calculées dans le serializer si nécessaire
        )

        if department:
            if user.is_manager:
                # assuré par StructureAdminPermission
                assert user.departments
                if department not in user.departments:
                    raise PermissionDenied
            structures = structures.filter(department=department)
        else:
            if user.is_manager:
                structures = structures.filter(department__in=user.departments)

        moderation = self.request.query_params.get("moderation") in TRUTHY_VALUES
        if moderation:
            return structures.exclude(moderation_status=ModerationStatus.VALIDATED)

        return structures

    def get_serializer_class(self):
        if self.action == "list":
            return StructureAdminListOptimizedSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        """
        Consolidation backend optimisée : parcourt toutes les pages côté backend
        et consolide les résultats avant d'envoyer au frontend.
        Utilise une approche intelligente pour éviter les problèmes de performance.
        """
        queryset = self.get_queryset()

        # Compter le total une seule fois
        total_count = queryset.count()
        page_size = 50
        total_pages = (total_count + page_size - 1) // page_size

        all_results = []

        # Traiter page par page avec des requêtes optimisées
        for page in range(total_pages):
            print(f"Page {page + 1}/{total_pages}")
            offset = page * page_size

            # Créer un nouveau queryset pour chaque page pour éviter l'accumulation
            page_queryset = self.get_queryset()[offset : offset + page_size]

            # Sérialiser chaque page indépendamment
            serializer = self.get_serializer(page_queryset, many=True)
            all_results.extend(serializer.data)

            # Libérer la mémoire explicitement
            del page_queryset

        return Response(all_results)


class ServiceAdminViewSet(
    ModerationMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ServiceAdminSerializer
    permission_classes = [ServiceAdminPermission]
    pagination_class = OptionalPageNumberPagination

    lookup_field = "slug"

    def get_queryset(self):
        moderation = self.request.query_params.get("moderation") in TRUTHY_VALUES
        all_services = Service.objects.select_related("structure").filter(
            status=ServiceStatus.PUBLISHED
        )
        if moderation:
            return all_services.exclude(moderation_status=ModerationStatus.VALIDATED)
        return all_services

    def get_serializer_class(self):
        if self.action == "list":
            return ServiceAdminListSerializer
        return super().get_serializer_class()
