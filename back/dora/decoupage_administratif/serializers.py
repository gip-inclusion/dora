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


class AdminDivisionSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    similarity = serializers.FloatField()
