# Generated by Django 4.2.1 on 2023-11-09 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0003_object_is_smart_alter_object_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='address',
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='object',
            name='number',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True, verbose_name='Номер объекта\\договора'),
        ),
    ]