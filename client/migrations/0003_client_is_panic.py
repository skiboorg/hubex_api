# Generated by Django 4.2.1 on 2023-07-21 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_dealer'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_panic',
            field=models.BooleanField(default=False),
        ),
    ]
