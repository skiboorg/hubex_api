# Generated by Django 4.2.1 on 2023-07-21 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_remove_user_is_panic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Название')),
                ('url', models.CharField(blank=True, max_length=20, null=True, verbose_name='Ссылка на страницу')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='PagePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Название доступа')),
                ('can_open', models.BooleanField(default=False)),
                ('can_edit', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RolePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.page')),
                ('permission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.pagepermission')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='user.role')),
            ],
        ),
    ]
