from operator import attrgetter

from django.contrib.gis.geos import Point
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Value
from rest_framework import exceptions, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_gis.fields import GeometrySerializerMethodField

from dora.admin_express.utils import normalize_string_for_search
from dora.core.constants import WGS84
from dora.core.utils import TRUTHY_VALUES

from .models import EPCI, AdminDivisionType, City, Department, Region


@api_view()
@permission_classes([permissions.AllowAny])
def search(request):
    class AdminDivisionSerializer(serializers.Serializer):
        code = serializers.CharField()
        name = serializers.CharField()
        similarity = serializers.FloatField()
        geom = GeometrySerializerMethodField()

        def __init__(self, *args, **kwargs):
            serialize_geom = kwargs.pop("with_geom", False)
            super().__init__(*args, **kwargs)
            if not serialize_geom:
                self.fields.pop("geom")

        def get_geom(self, obj):
            return obj.geom.simplify(tolerance=0.1)

    type = request.GET.get("type", "")
    with_geom = request.GET.get("with_geom", False) in TRUTHY_VALUES
    q = request.GET.get("q", "")
    if not type or not q:
        raise exceptions.ValidationError("type and q are required")
    norm_q = normalize_string_for_search(q)

    Model = None
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
    if not with_geom:
        qs = qs.defer("geom")

    return Response(AdminDivisionSerializer(qs, many=True, with_geom=with_geom).data)


@api_view()
@permission_classes([permissions.AllowAny])
def reverse_search(request):
    class AdminDivisionSerializer(serializers.Serializer):
        code = serializers.CharField()
        name = serializers.CharField()

    type = request.GET.get("type")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    if not type or not lat or not lon:
        raise exceptions.ValidationError("type, lat and lon are required")
    point = Point(float(lon), float(lat), srid=WGS84)

    Model = None
    if type == AdminDivisionType.CITY:
        Model = City
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

    result = Model.objects.filter(geom__covers=point).first()
    if result is not None:
        return Response(AdminDivisionSerializer(result).data)
    raise NotFound


@api_view()
@permission_classes([permissions.AllowAny])
def get_city_label(request, insee_code):
    city = City.objects.get_from_code(insee_code)
    if city:
        return Response(city.name)
    raise NotFound


@api_view()
@permission_classes([permissions.AllowAny])
def get_departments(request):
    class DeptSerializer(serializers.Serializer):
        code = serializers.CharField()
        name = serializers.CharField()
        geom = GeometrySerializerMethodField()

        def get_geom(self, obj):
            return obj.geom.simplify(tolerance=0.1)

    q = request.GET.get("dept_codes", "")
    if q:
        departments = [Department.objects.get_from_code(code) for code in q.split(",")]
    else:
        departments = Department.objects.all()

    return Response(
        DeptSerializer(sorted(departments, key=attrgetter("code")), many=True).data
    )
