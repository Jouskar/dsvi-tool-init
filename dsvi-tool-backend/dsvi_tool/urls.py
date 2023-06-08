"""dsvi_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from geo.views import login_view
from geo.models import VectorModel, RasterModel, PointModel, LayerTypesModel, FeatureModel
from ml_util.models import MLModel
from rest_framework import routers, serializers, viewsets, generics
from rest_framework.response import Response
from geo import views

# Serializers define the API representation.


class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = 'geojson_str'


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureModel
        fields = ('geometry', 'properties',)


class VectorSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    @staticmethod
    def get_features(vector):
        features = FeatureModel.objects.filter(vector=vector)
        serializer = FeatureSerializer(features, many=True)
        return serializer.data

    class Meta:
        model = VectorModel
        fields = ('geojson_str', 'features',)


class LayerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerTypesModel
        fields = ('name', 'description',)


# ViewSets define the view behavior.

class LayerTypeViewSet(generics.ListAPIView):
    serializer_class = LayerTypeSerializer

    def get_queryset(self):
        queryset = LayerTypesModel.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VectorViewSet(generics.ListAPIView):
    serializer_class = VectorSerializer

    def get_queryset(self):
        queryset = VectorModel.objects.all()

        country = self.request.query_params.get('country')
        layer = self.request.query_params.get('layer')

        queryset = queryset.filter(country=country, layer_type__name=layer)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(serializer)
        return Response(serializer.data)


class MLModelViewSet(generics.ListAPIView):
    serializer_class = MLModelSerializer

    def get_queryset(self):
        queryset = MLModel.objects.all()

        vector_model_1 = self.request.query_params.get('vector1')
        vector_model_2 = self.request.query_params.get('vector2')

        #queryset = queryset.filter(vector_model1=VectorModel.objects.get(name=vector_model_1), vector_model2=VectorModel.objects.get(name=vector_model_2))
        analysis = MLModel()
        analysis.calculate_similarity(VectorModel.objects.get(name=vector_model_1), VectorModel.objects.get(name=vector_model_2))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('vector/', VectorViewSet.as_view()),
    path('layer-types/', LayerTypeViewSet.as_view()),
    path('vector-ml/', MLModelViewSet.as_view()),
    # path('api/login/', login_view()),
    path('login', views.login_view, name='login'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
