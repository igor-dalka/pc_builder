# Generated by Django 5.2.2 on 2025-06-15 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0011_cpu_tdp_oc'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu',
            name='average_max_oc',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
