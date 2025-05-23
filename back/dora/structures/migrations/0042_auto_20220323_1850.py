# Generated by Django 3.2.12 on 2022-03-23 17:50

from django.db import migrations, models

import dora.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0041_alter_structure_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="structure",
            name="siret",
            field=models.CharField(
                blank=True,
                max_length=14,
                null=True,
                unique=True,
                validators=[dora.core.validators.validate_siret],
                verbose_name="Siret",
            ),
        ),
        migrations.AddConstraint(
            model_name="structure",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("siret__isnull", False), ("parent__isnull", False), _connector="OR"
                ),
                name="structures_structure_null_siret_only_in_branches",
            ),
        ),
        migrations.AddConstraint(
            model_name="structure",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("parent__isnull", True),
                    models.Q(("branch_id", ""), _negated=True),
                    _connector="OR",
                ),
                name="structures_structure_branches_have_id",
            ),
        ),
    ]
