# Generated by Django 5.0.1 on 2024-01-08 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioAPP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='addresse',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]