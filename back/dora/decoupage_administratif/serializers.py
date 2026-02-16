from rest_framework import serializers

from dora.decoupage_administratif.models import AdminDivisionType


class SearchQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=[
            AdminDivisionType.CITY,
            AdminDivisionType.EPCI,
            AdminDivisionType.DEPARTMENT,
            AdminDivisionType.REGION,
        ],
        required=True,
    )
    q = serializers.CharField(required=True)


class ReverseSearchQuerySerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=[
            AdminDivisionType.CITY,
            AdminDivisionType.EPCI,
            AdminDivisionType.DEPARTMENT,
            AdminDivisionType.REGION,
        ],
        required=True,
    )
    lat = serializers.FloatField(required=True)
    lon = serializers.FloatField(required=True)


class ReverseSearchAdminDivisionSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class GetDepartmentsQuerySerializer(serializers.Serializer):
    dept_codes = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_dept_codes(self, value):
        if not value or not value.strip():
            return []
        return [c.strip().upper() for c in value.split(",") if c.strip()]


class AdminDivisionSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()


class AdminDivisionSearchResultSerializer(AdminDivisionSerializer):
    similarity = serializers.FloatField()
