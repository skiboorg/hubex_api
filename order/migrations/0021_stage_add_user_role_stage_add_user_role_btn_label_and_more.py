# Generated by Django 4.2.1 on 2023-07-07 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_user_channel_user_is_online'),
        ('order', '0020_order_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='add_user_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='add_user_role', to='user.role'),
        ),
        migrations.AddField(
            model_name='stage',
            name='add_user_role_btn_label',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='is_add_user_required',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='stage',
            name='need_add_user',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
