# Generated by Django 4.2.1 on 2023-09-01 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_alter_userworktime_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telega',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Телега'),
        ),
    ]
