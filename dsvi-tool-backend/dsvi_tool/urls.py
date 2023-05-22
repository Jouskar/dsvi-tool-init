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
from geo.models import VectorModel, RasterModel, PointModel, LayerTypesModel
from rest_framework import routers, serializers, viewsets, generics
from rest_framework.response import Response


# Serializers define the API representation.
class VectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorModel
        fields = ('data_geojson',)


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
        return Response(serializer.data)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('vector/', VectorViewSet.as_view()),
    path('layer-types/', LayerTypeViewSet.as_view()),
    # path('api/login/', login_view()),
    path('login', auth_views.LoginView.as_view(), name='login'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
