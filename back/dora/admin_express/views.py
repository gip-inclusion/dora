from django.contrib.gis.geos import Point
from rest_framework import exceptions, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import AdminDivisionType

from .models import EPCI, City, Department, Region


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
