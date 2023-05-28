from django.contrib import admin
from django import forms
from django.contrib.gis.geos import GeometryCollection, GEOSGeometry, MultiPolygon
from django.contrib.gis.gdal import GDALRaster, DataSource, OGRGeometry
from geo.models import *
import json


def change_property_key(property_key: str):
    if property_key == 'NAME_1':
        return 'name'
    else:
        return property_key.lstrip('_')


class VectorJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, dict):
            include_fields = ['type', 'features']
            new_obj = {key: value for key, value in obj.items() if key in include_fields}
            return new_obj
        return super().default(obj)


class VectorForm(forms.ModelForm):
    vector_file = forms.FileField()

    class Meta:
        model = VectorModel
        fields = ('name', 'vector_file', 'layer_type', 'country', 'region',
                  'administrative_level', 'critique_value', 'editor', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['layer_type'].widget = forms.Select(choices=self.get_layer_type_choices())
        self.fields['region'].required = False

    @staticmethod
    def get_layer_type_choices():
        choices = [(layer_type.id, layer_type.name) for layer_type in LayerTypesModel.objects.all()]
        return choices

    def save(self, commit=True):
        instance = super().save(commit=False)
        geojson_file = self.cleaned_data.get('vector_file')
        if geojson_file:
            geojson_string = json.load(geojson_file)
            # print(features_geometry)
            instance.geojson_str = json.dumps(geojson_string)
        if commit:
            instance.save()
            geojson_string = json.load(geojson_file)
            data_source = DataSource(json.dumps(geojson_string), ds_driver='GeoJSON')
            print('coutn', data_source)
            for feature in data_source[0]:
                geometry = feature.geom
                properties = {change_property_key(field): feature.get(field)
                              for field in feature.fields if field != 'NAME'}
                new_feature = FeatureModel(geometry=geometry.geos, properties=properties)
                for key, value in properties.items():
                    setattr(new_feature, key, value)
                print('Geometry:', geometry)
                print('Properties:', properties)
                new_feature.vector
                new_feature.save()
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


@admin.register(LayerTypesModel)
class LayerTypesAdmin(admin.ModelAdmin):
    pass
