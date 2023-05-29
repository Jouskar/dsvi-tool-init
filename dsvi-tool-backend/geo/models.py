from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from django.contrib.auth.models import User
from django.contrib.gis.gdal import GDALRaster, DataSource, OGRGeometry
import json
from django.utils.translation import gettext_lazy as _


# Datasets should be sent via the rest framework to the react frontend
# Options are mainly affected by Leaflet options, so that should be handled via state through the frontend
# The type information is important enough to be passed to the front-end alongside the dataset
# Minimize total load on the front-end in terms of displaying the larger datasets by possibly adding a size field? TODO

def change_property_key(property_key: str):
    if property_key == 'NAME_1':
        return 'name_1'
    elif property_key == 'NAME_2':
        return 'name_2'
    else:
        return property_key.lstrip('_')


class Status(models.IntegerChoices):
    DELETED = -1, "Deleted"
    PENDING = 0, "Pending"
    ACTIVE = 1, "Active"


class LayerTypesModel(models.Model):
    name = models.CharField(max_length=240)
    description = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )


class VectorModel(models.Model):
    name = models.CharField(max_length=240)
    vector_file = models.FileField()
    geojson_str = models.CharField()
    layer_type = models.ForeignKey(
        LayerTypesModel,
        null=True,
        on_delete=models.SET_NULL,
    )
    critique_value = models.IntegerField(default=0)
    data_date = models.DateTimeField(
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=200)
    region = models.CharField(
        max_length=200,
        null=True,
    )
    administrative_level = models.IntegerField()
    editor = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        data_source = DataSource(self.geojson_str, ds_driver='GeoJSON')
        for feature in data_source[0]:
            geometry = feature.geom
            properties = {change_property_key(field): feature.get(field)
                          for field in feature.fields if field != 'NAME'}
            new_feature = FeatureModel(geometry=geometry.geos, properties=properties)
            for key, value in properties.items():
                setattr(new_feature, key, value)
            new_feature.vector = self
            new_feature.save()


class FeatureModel(models.Model):
    geometry = models.MultiPolygonField()
    properties = models.JSONField()
    name_1 = models.CharField()
    name_2 = models.CharField(default='')
    count = models.FloatField(null=True)
    sum = models.FloatField(null=True)
    mean = models.FloatField(null=True)
    median = models.FloatField(null=True)
    stdev = models.FloatField(null=True)
    min = models.FloatField(null=True)
    max = models.FloatField(null=True)
    range = models.FloatField(null=True)
    minority = models.FloatField(null=True)
    majority = models.FloatField(null=True)
    vector = models.ForeignKey(VectorModel, on_delete=models.CASCADE)


class RasterModel(models.Model):
    name = models.CharField(max_length=240)
    data = models.RasterField(
        verbose_name="Raster data",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    styling = JSONField()
    editor = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )


class PointModel(models.Model):
    name = models.CharField(max_length=240)
    data = models.RasterField(
        verbose_name="Point data",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    styling = JSONField()
    editor = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )


'''class Dataset(models.Model):
    class Type(models.TextChoices):
        POINT = 'PT', _('Point')
        RASTER = 'RT', _('Raster')
        VECTOR = 'VT', _('Vector')

    fileName = models.CharField("file_name", max_length=240)
    name = models.CharField("name", max_length=240)
    type = models.CharField(
        max_length=2,
        choices=Type.choices,
        default=Type.POINT  # Default as point data?
    )

    def __str__(self):
        return self.name'''
