# Generated by Django 4.2.1 on 2023-06-29 11:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_order_options_checklistinput_input_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4),
        ),
    ]
