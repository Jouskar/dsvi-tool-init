from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Dataset
from .serializers import *


# Create your views here.

@api_view(['GET', 'POST'])
def datasets_list(request):
    if (request.method == 'GET'):
        data = Dataset.objects.all()
        serializer = DatasetSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)


@api_view['PUT', 'DELETE']
def datasets_detail(request, pk):
    try:
        dataset = Dataset.objects.get(pk=pk)
    except Dataset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# break down into chunks TODO
@api_view['GET']
def dataset_file(request, pk):
    dataset = Dataset.objects.get(1)
    try:
        dataset = Dataset.objects.get(pk=pk)
    except Dataset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    file = open("datasets/" + dataset.type.label + "/" + dataset.fileName)
    response = HttpResponse(FileWrapper(file), content_type='application/json')
    return response
