from rest_framework import serializers


class AdminDivisionSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    similarity = serializers.FloatField()
