# Generated by Django 4.2.14 on 2024-07-13 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CentreSportif', '0017_alter_horaire_jour'),
    ]

    operations = [
        migrations.AddField(
            model_name='moniteur',
            name='password',
            field=models.CharField(default='default_password', max_length=255),
        ),
        migrations.AddField(
            model_name='moniteur',
            name='user',
            field=models.CharField(default='winners', max_length=255),
            preserve_default=False,
        ),
    ]
