# Generated by Django 4.2.1 on 2023-06-18 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0002_object_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='object/images')),
                ('text', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='object',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='object/image'),
        ),
        migrations.DeleteModel(
            name='ObjectImage',
        ),
        migrations.AddField(
            model_name='objectfile',
            name='object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='object.object'),
        ),
    ]
