from django.db import migrations
from django.utils import timezone


def delete_expired_tokens(apps, _):
    Token = apps.get_model("rest_auth", "Token")
    expired_tokens = Token.objects.filter(expiration__lt=timezone.now())
    expired_tokens.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("rest_auth", "0003_add_token_expiration_date"),
    ]

    operations = [
        migrations.RunPython(delete_expired_tokens, migrations.RunPython.noop)
    ]
