from django.contrib.gis.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Datasets should be sent via the rest framework to the react frontend
# Options are mainly affected by Leaflet options, so that should be handled via state through the frontend
# The type information is important enough to be passed to the front-end alongside the dataset
# Minimize total load on the front-end in terms of displaying the larger datasets by possibly adding a size field? TODO
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
    data_geojson = models.CharField(
        null=True,
    )
    data = models.MultiPolygonField(
        verbose_name="Vector data",
        null=True,
    )
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


class FeatureCityModel(models.Model):
    name = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
