from rest_framework import serializers

from dora.services.models import Bookmark, SavedSearch
from dora.services.serializers import BookmarkListSerializer, SavedSearchSerializer
from dora.sirene.models import Establishment
from dora.structures.models import Structure
from dora.structures.serializers import StructureListSerializer
from dora.users.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    short_name = serializers.CharField(source="get_short_name", read_only=True)
    structures = serializers.SerializerMethodField()
    pending_structures = serializers.SerializerMethodField()
    bookmarks = serializers.SerializerMethodField()
    saved_searches = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "bookmarks",
            "departments",
            "email",
            "first_name",
            "full_name",
            "is_manager",
            "is_staff",
            "last_name",
            "newsletter",
            "pending_structures",
            "saved_searches",
            "short_name",
            "structures",
            "main_activity",
            "cgu_versions_accepted",
        ]

    def get_structures(self, user):
        if not user or not user.is_authenticated:
            qs = Structure.objects.none()
        else:
            qs = Structure.objects.filter(membership__user=user).prefetch_related(
                "services"
            )
        return StructureListSerializer(qs, many=True, context={"user": user}).data

    def get_pending_structures(self, user):
        if not user or not user.is_authenticated:
            qs = Structure.objects.none()
        else:
            qs = Structure.objects.filter(
                putative_membership__user=user,
                putative_membership__invited_by_admin=False,
            )
        return StructureListSerializer(qs, many=True, context={"user": user}).data

    def get_bookmarks(self, user):
        if not user or not user.is_authenticated:
            qs = Bookmark.objects.none()
        else:
            qs = Bookmark.objects.filter(user=user).order_by("-creation_date")
        return BookmarkListSerializer(qs, many=True).data

    def get_saved_searches(self, user):
        if not user or not user.is_authenticated:
            qs = SavedSearch.objects.none()
        else:
            qs = SavedSearch.objects.filter(user=user).order_by("-creation_date")
        return SavedSearchSerializer(qs, many=True).data


class TokenSerializer(serializers.Serializer):
    key = serializers.CharField()


class JoinStructureSerializer(serializers.Serializer):
    siret = serializers.CharField(required=False)
    structure_slug = serializers.CharField(required=False)
    cgu_version = serializers.CharField(required=True)
    fast_track = serializers.BooleanField(required=False, default=False)

    def validate(self, data):
        siret = data.get("siret")
        structure_slug = data.get("structure_slug")
        if siret and structure_slug:
            raise serializers.ValidationError(
                "`siret` et `structure_slug` ne peuvent être présents simultanément"
            )
        if siret:
            try:
                establishment = Establishment.objects.get(siret=siret)
                data["establishment"] = establishment
            except Establishment.DoesNotExist:
                # The field is hidden on the frontend, so display this error globally
                # TODO: Ideally it should be the frontend role to display the message anyway
                raise serializers.ValidationError({"non_field_errors": "SIRET inconnu"})
        else:
            try:
                structure = Structure.objects.get(slug=structure_slug)
                data["structure"] = structure
            except Structure.DoesNotExist:
                # The field is hidden on the frontend, so display this error globally
                # TODO: Ideally it should be the frontend role to display the message anyway
                raise serializers.ValidationError(
                    {"non_field_errors": "structure inconnue"}
                )
        return super().validate(data)
