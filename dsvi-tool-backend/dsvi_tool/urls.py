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
from geo.models import VectorModel, RasterModel, PointModel
from rest_framework import routers, serializers, viewsets, generics


# Serializers define the API representation.
class VectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorModel
        fields = ('data_geojson',)


# ViewSets define the view behavior.
class VectorViewSet(generics.ListCreateAPIView):
    queryset = VectorModel.objects.all()
    serializer_class = VectorSerializer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('vector/', VectorViewSet.as_view()),
    # path('api/login/', login_view()),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
