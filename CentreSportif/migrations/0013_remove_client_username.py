# Generated by Django 5.0.6 on 2024-06-28 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CentreSportif', '0012_client_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='username',
        ),
    ]
