# Generated by Django 4.2.1 on 2023-11-02 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_alter_equipment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='is_temp_equipment',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
