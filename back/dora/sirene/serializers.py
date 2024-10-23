from rest_framework import serializers

from .models import Establishment


class EstablishmentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = [
            "address1",
            "address2",
            "ape",
            "city",
            "city_code",
            "is_siege",
            "latitude",
            "longitude",
            "name",
            "postal_code",
            "siren",
            "siret",
        ]

    def get_name(self, obj):
        if not obj.name:
            return obj.parent_name

        if obj.name.startswith(obj.parent_name) or obj.parent_name.startswith(obj.name):
            return obj.name

        return f"{obj.name} ({obj.parent_name})"[:255]
