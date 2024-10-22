from django.contrib.gis.geos import Point
from django.db import migrations


def to_point(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Service = apps.get_model("services", "Service")
    for service in Service.objects.all():
        if service.longitude and service.latitude:
            service.geom = Point(service.longitude, service.latitude, srid=4326)
            service.save()


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0018_service_geom"),
    ]

    operations = [
        migrations.RunPython(to_point),
    ]
