# Generated by Django 4.2.1 on 2023-07-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0010_alter_equipmentmodel_firm'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='is_warranty',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='equipment',
            name='warranty_ends',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]