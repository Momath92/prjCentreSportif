# Generated by Django 5.0.6 on 2024-06-27 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CentreSportif', '0006_activite_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
