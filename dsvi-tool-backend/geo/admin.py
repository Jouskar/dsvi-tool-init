from django.contrib import admin
from django import forms
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import GDALRaster
from geo.models import VectorModel, RasterModel, PointModel
import json


class VectorForm(forms.ModelForm):
    vector_file = forms.FileField()

    class Meta:
        model = VectorModel
        fields = ('name', 'vector_file', 'country', 'region', 'administrative_level', 'editor', 'status')

    def save(self, commit=True):
        instance = super().save(commit=False)
        geojson_file = self.cleaned_data.get('vector_file')
        if geojson_file:
            # geojson_raw = geojson_file.read().decode('utf-8')
            geojson_string = json.load(geojson_file)
            print("hebe")
            print(json.dumps(geojson_string))
            # geometry = GEOSGeometry(json.dumps(geojson_string), srid=4326)
            instance.data_geojson = json.dumps(geojson_string)
        if commit:
            instance.save()
        return instance


class RasterForm(forms.ModelForm):
    raster_file = forms.FileField()

    class Meta:
        model = RasterModel
        fields = ('name', 'raster_file', 'country', 'region', 'styling', 'editor', 'status')

    def save(self, commit=True):
        instance = super().save(commit=False)
        raster_file = self.cleaned_data.get('raster_file')
        if raster_file:
            raster = GDALRaster(raster_file)
            instance.dataa = json.dumps(raster)
        if commit:
            instance.save()
        return instance


@admin.register(VectorModel)
class VectorAdmin(admin.ModelAdmin):
    form = VectorForm


@admin.register(RasterModel)
class RasterAdmin(admin.ModelAdmin):
    form = RasterForm


@admin.register(PointModel)
class PointAdmin(admin.ModelAdmin):
    pass
