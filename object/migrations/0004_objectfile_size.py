# Generated by Django 4.2.1 on 2023-06-18 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0003_objectfile_object_image_delete_objectimage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectfile',
            name='size',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
