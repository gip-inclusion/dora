from dora.stats.models import SearchType

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchview",
            name="keyword",
            field=models.CharField(blank=True, verbose_name="Mots-clés saisis"),
        ),
        migrations.AddField(
            model_name="searchview",
            name="search_type",
            field=models.CharField(
                choices=SearchType.choices,
                default=SearchType.THEMATIQUE,
                max_length=20,
                verbose_name="Type de recherche",
            ),
            preserve_default=False,
        ),
    ]
