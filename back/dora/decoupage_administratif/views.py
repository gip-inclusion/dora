from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Value
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from dora.decoupage_administratif.models import AdminDivisionType
from dora.decoupage_administratif.utils import normalize_string_for_search

from .models import EPCI, City, Department, Region
from .serializers import (
    AdminDivisionSearchResultSerializer,
    AdminDivisionSerializer,
    GetDepartmentsQuerySerializer,
    SearchQuerySerializer,
)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def search(request):
    serializer = SearchQuerySerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)

    type = serializer.validated_data["type"]
    q = serializer.validated_data["q"].upper()
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

    if q.isdigit() or q.startswith("2A") or q.startswith("2B"):
        qs = (
            Model.objects.filter(code__startswith=q)
            .annotate(similarity=Value(1))
            .order_by(*sort_fields, "normalized_name")[:10]
        )
    else:
        qs = (
            Model.objects.annotate(
                similarity=TrigramSimilarity("normalized_name", norm_q)
            )
            .filter(similarity__gt=0.1 if len(q) > 3 else 0)
            .order_by(*sort_fields)[:10]
        )

    return Response(AdminDivisionSearchResultSerializer(qs, many=True).data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_departments(request):
    serializer = GetDepartmentsQuerySerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)

    codes = serializer.validated_data["dept_codes"]
    if codes:
        departments = Department.objects.filter(code__in=codes).order_by("code")
    else:
        departments = Department.objects.all().order_by("code")

    return Response(AdminDivisionSerializer(departments, many=True).data)
