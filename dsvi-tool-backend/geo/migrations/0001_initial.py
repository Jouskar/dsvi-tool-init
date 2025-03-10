# Generated by Django 4.2 on 2023-05-29 13:02

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LayerTypesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('description', models.CharField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(-1, 'Deleted'), (0, 'Pending'), (1, 'Active')], default=0, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='VectorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('vector_file', models.FileField(upload_to='')),
                ('geojson_str', models.CharField()),
                ('critique_value', models.IntegerField(default=0)),
                ('data_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200, null=True)),
                ('administrative_level', models.IntegerField()),
                ('status', models.IntegerField(choices=[(-1, 'Deleted'), (0, 'Pending'), (1, 'Active')], default=0, verbose_name='Status')),
                ('editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('layer_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='geo.layertypesmodel')),
            ],
        ),
        migrations.CreateModel(
            name='RasterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('data', django.contrib.gis.db.models.fields.RasterField(srid=4326, verbose_name='Raster data')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200)),
                ('styling', models.JSONField()),
                ('status', models.IntegerField(choices=[(-1, 'Deleted'), (0, 'Pending'), (1, 'Active')], default=0, verbose_name='Status')),
                ('editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PointModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('data', django.contrib.gis.db.models.fields.RasterField(srid=4326, verbose_name='Point data')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200)),
                ('styling', models.JSONField()),
                ('status', models.IntegerField(choices=[(-1, 'Deleted'), (0, 'Pending'), (1, 'Active')], default=0, verbose_name='Status')),
                ('editor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('properties', models.JSONField()),
                ('name', models.CharField()),
                ('count', models.FloatField()),
                ('sum', models.FloatField()),
                ('mean', models.FloatField()),
                ('median', models.FloatField()),
                ('stdev', models.FloatField()),
                ('min', models.FloatField()),
                ('max', models.FloatField()),
                ('range', models.FloatField()),
                ('minority', models.FloatField()),
                ('majority', models.FloatField()),
                ('vector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.vectormodel')),
            ],
        ),
    ]
