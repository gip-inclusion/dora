from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0007_recompute_sync_checksums"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="service",
            name="beneficiaries_access_modes",
        ),
        migrations.RemoveField(
            model_name="service",
            name="beneficiaries_access_modes_external_form_link",
        ),
        migrations.RemoveField(
            model_name="service",
            name="beneficiaries_access_modes_external_form_link_text",
        ),
        migrations.RemoveField(
            model_name="service",
            name="beneficiaries_access_modes_other",
        ),
        migrations.RemoveField(
            model_name="service",
            name="coach_orientation_modes",
        ),
        migrations.RemoveField(
            model_name="service",
            name="coach_orientation_modes_external_form_link",
        ),
        migrations.RemoveField(
            model_name="service",
            name="coach_orientation_modes_external_form_link_text",
        ),
        migrations.RemoveField(
            model_name="service",
            name="coach_orientation_modes_other",
        ),
        migrations.DeleteModel(
            name="BeneficiaryAccessMode",
        ),
        migrations.DeleteModel(
            name="CoachOrientationMode",
        ),
    ]
