# Generated by Django 4.2.1 on 2023-07-17 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.TextField(blank=True, null=True),
        ),
    ]