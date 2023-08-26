# from django.shortcuts import render
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
def journal_list(request, domainname):
    # mt_id = _getmt(domainname)
    if request.method == 'GET':
        journal_list = Journal.objects.all()
        serializer = JournalSerializer(journal_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)
    elif request.method == 'POST':
        data = request.data
        # data['mt'] = mt_id
        serializer = JournalSerializer(data=data)
        if serializer.is_valid():
            new_journal = serializer.save()
            return Response(model_to_dict(new_journal), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
def journal(request, domainname, journal_id):
    # mt_id = _getmt(domainname)
    if request.method == 'DELETE':
        journal = Journal.objects.filter(id=journal_id)
        journal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        data = request.data
        # data['mt'] = mt_id
        serializer = JournalSerializer(data=data)
        if serializer.is_valid():
            Journal.objects.filter(id=journal_id).update(**data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)