from operator import attrgetter

from django.contrib.gis.geos import Point
from rest_framework import exceptions, permissions, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_gis.fields import GeometrySerializerMethodField

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import AdminDivisionType

from .models import EPCI, City, Department, Region


class DeptSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    geom = GeometrySerializerMethodField()

    def get_geom(self, obj):
        """Simplifie la géométrie en s'assurant qu'elle reste valide.

        Essaie différentes valeurs de tolérance de manière progressive :
        - 0.1 : simplification agressive (moins de points)
        - 0.05 : simplification moyenne
        - 0.01 : simplification légère
        - 0.005 : simplification très légère
        Si aucune simplification ne fonctionne, retourne la géométrie originale.
        """
        # Liste des tolérances à essayer, de la plus agressive à la plus conservative
        tolerances = [0.1, 0.05, 0.01, 0.005]

        for tolerance in tolerances:
            simplified = obj.geom.simplify(tolerance=tolerance)
            # Vérifie que la géométrie n'est pas vide et a la bonne structure
            if not simplified.empty and simplified.geom_type in [
                "Polygon",
                "MultiPolygon",
            ]:
                return simplified

        # Si aucune simplification n'a fonctionné, retourner la géométrie originale
        return obj.geom


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
    q = request.GET.get("dept_codes", "")
    if q:
        departments = [Department.objects.get_from_code(code) for code in q.split(",")]
    else:
        departments = Department.objects.all()

    return Response(
        DeptSerializer(sorted(departments, key=attrgetter("code")), many=True).data
    )
