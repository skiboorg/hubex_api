# Generated by Django 4.2.1 on 2023-11-16 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_stagegroupselect_delete_stagefirmselect'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон'),
        ),
    ]
