from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import City


@api_view()
@permission_classes([permissions.AllowAny])
def get_city_label(request, insee_code):
    city = City.objects.get_from_code(insee_code)
    if city:
        return Response(city.name)
    raise NotFound
