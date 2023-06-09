# Generated by Django 4.2.1 on 2023-06-12 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('object', '0001_initial'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckListData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckListInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='InputField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_boolean', models.BooleanField(default=False, null=True)),
                ('is_input', models.BooleanField(default=False, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Статус ',
                'verbose_name_plural': 'Статус ',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('is_check_list_done', models.BooleanField(default=False, null=True)),
                ('btn_1_goto_stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goto_stage_1_btn', to='order.stage')),
                ('btn_2_goto_stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goto_stage_2_btn', to='order.stage')),
                ('check_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.checklist')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=255, null=True)),
                ('is_critical', models.BooleanField(blank=True, default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('date_created_at', models.DateField(blank=True, null=True)),
                ('date_assign_worker', models.DateField(blank=True, null=True)),
                ('date_done', models.DateField(blank=True, null=True)),
                ('date_dead_line', models.DateField(blank=True, null=True)),
                ('equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='equipment.equipment')),
                ('object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='object.object')),
                ('stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.stage')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.status')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]
