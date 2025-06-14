# Generated by Django 5.2.2 on 2025-06-10 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0003_chassis_cpu_cooler_disc_fan_thermal_paste_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphicscard',
            name='tdp',
            field=models.IntegerField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='thermal_paste',
            name='conductivity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
