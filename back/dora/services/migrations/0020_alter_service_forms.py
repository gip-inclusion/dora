import django.contrib.postgres.fields
from django.db import migrations, models

import dora.services.models


def deduplicate_form_names(apps, schema_editor):
    """Écarte les documents en double avant l'entrée en vigueur du validateur.

    Seul le nom de fichier est affiché à l'utilisateur : deux clés dont le nom
    coïncide sont indistinguables dans le formulaire. On conserve la première
    occurrence et on retire les suivantes de la liste (les fichiers stockés ne
    sont pas supprimés, ils peuvent être référencés ailleurs).
    """
    Service = apps.get_model("services", "Service")

    services_to_update = []
    for service in (
        Service._base_manager.exclude(forms=[]).only("id", "forms").iterator()
    ):
        seen_names = set()
        deduplicated_forms = []
        for form in service.forms:
            name = form.rsplit("/", 1)[-1]
            if name in seen_names:
                continue
            seen_names.add(name)
            deduplicated_forms.append(form)

        if deduplicated_forms != service.forms:
            service.forms = deduplicated_forms
            services_to_update.append(service)

    Service.objects.bulk_update(services_to_update, ["forms"], batch_size=500)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0019_service_horaires_accueil"),
    ]

    operations = [
        migrations.RunPython(
            deduplicate_form_names, reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="service",
            name="forms",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=1024),
                blank=True,
                default=list,
                validators=[dora.services.models.validate_unique_form_names],
                verbose_name="Partagez les documents à compléter",
            ),
        ),
    ]
