"""Add missing db indexes for frequently-filtered fields.

This migration ensures indexes exist for fields that are often used
in WHERE clauses and grouping operations.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("environment", "0003_environmentaldata"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="marineprotectedarea",
            index=models.Index(fields=["governance_type"], name="env_mpa_gov_idx"),
        ),
        migrations.AddIndex(
            model_name="marineprotectedarea",
            index=models.Index(fields=["management_authority"], name="env_mpa_mgmt_idx"),
        ),
    ]
