from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_dora_bot_user(apps, schema_editor):
    """Crée l'utilisateur dora bot."""
    User = apps.get_model("users", "User")

    # Le modèle historique n'a pas les méthodes Nexus.
    # On les patche pour que save() ne lève pas d'exception.
    User.should_sync_to_nexus = lambda self: False
    User.nexus_delete = lambda *args, **kwargs: None
    User.nexus_sync = lambda *args, **kwargs: None

    User.objects.get_or_create(
        email=settings.DORA_BOT_USER.lower(),
        defaults={
            "last_name": "Bot",
            "first_name": "Dora",
            "is_staff": True,
            "is_active": False,
            "is_valid": True,
            "password": make_password(None),
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_dora_bot_user, reverse_code=migrations.RunPython.noop
        ),
    ]
