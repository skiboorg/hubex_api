# Generated by Django 4.2.1 on 2023-08-30 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0013_equipment_is_service_book_sign'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='service_book_sign_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]