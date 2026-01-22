from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Value
from rest_framework import exceptions, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from dora.admin_express.models import AdminDivisionType
from dora.admin_express.utils import normalize_string_for_search

from .models import EPCI, City, Department, Region


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def search(request):
    class AdminDivisionSerializer(serializers.Serializer):
        code = serializers.CharField()
        name = serializers.CharField()
        similarity = serializers.FloatField()

    type = request.GET.get("type", "")
    q = request.GET.get("q", "")
    if not type or not q:
        raise exceptions.ValidationError("type and q are required")
    norm_q = normalize_string_for_search(q)

    sort_fields = ["-similarity"]
    if type == AdminDivisionType.CITY:
        Model = City
        sort_fields = ["-similarity", "-population"]
    elif type == AdminDivisionType.EPCI:
        Model = EPCI
    elif type == AdminDivisionType.DEPARTMENT:
        Model = Department
    elif type == AdminDivisionType.REGION:
        Model = Region
    else:
        raise exceptions.ValidationError(
            f"Invalid type, expected one of {AdminDivisionType.CITY}, {AdminDivisionType.EPCI}, {AdminDivisionType.DEPARTMENT}, {AdminDivisionType.REGION}"
        )

    if q.isdigit() or q == "2A" or q == "2B":
        qs = (
            Model.objects.filter(code__startswith=q)
            .annotate(similarity=Value(1))
            .order_by(*sort_fields, "code")[:10]
        )
    else:
        qs = (
            Model.objects.annotate(
                similarity=TrigramSimilarity("normalized_name", norm_q)
            )
            .filter(similarity__gt=0.1 if len(q) > 3 else 0)
            .order_by(*sort_fields)[:10]
        )

    return Response(AdminDivisionSerializer(qs, many=True).data)
