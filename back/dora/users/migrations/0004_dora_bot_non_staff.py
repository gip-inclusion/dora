from django.conf import settings
from django.db import migrations


def remove_dora_bot_staff(apps, schema_editor):
    """Retire le statut staff du compte dora bot, inutile à ses usages."""
    User = apps.get_model("users", "User")
    User.objects.filter(email=settings.DORA_BOT_USER.lower()).update(is_staff=False)


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_discovery_method"),
    ]

    operations = [
        migrations.RunPython(
            remove_dora_bot_staff, reverse_code=migrations.RunPython.noop
        ),
    ]
