from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
# from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework import status
# Create your views here.


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        product_list = Product.objects.all()
        serializer = ProductSerializer(product_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def cat_list(request):
    if request.method == 'GET':
        cat_list = Cat.objects.all().distinct('cat0')
        serializer = CatSerializer(cat_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)
    elif request.method == 'POST':
        # implement filtering
        # serializer = CatSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        selected_cat = data.get('selectedCat')
        cat_level = data.get('catLevelRequested')
        if cat_level == 1:
            if selected_cat == 'all':
                cat_list = Cat.objects.all().distinct('cat1')
            else:
                cat_list = Cat.objects.all().filter(cat0=selected_cat).distinct('cat1')
        elif cat_level == 2:
            cat_list = Cat.objects.all().filter(cat1=selected_cat).distinct('cat2')
        serializer = CatSerializer(cat_list, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def nugget_list(request):
    if request.method == 'GET':
        cat_list = Nugget.objects.all()
        serializer = NuggetSerializer(cat_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)
    elif request.method == 'POST':
        # implement filtering
        data = request.data
        selected_cat = data.get('cat')
        cat_level = data.get('catLevel')
        if cat_level == 1:
            # selected_cat_des = selected_cat.get('cat0')
            if selected_cat.get('cat0') == 'all':
                cat_list = Nugget.objects.all()
            else:
                cat_list = Nugget.objects.all().filter(nuggetcat__cat__cat0=selected_cat.get('cat0'))
        elif cat_level == 2:
            selected_cat_des = selected_cat.get('cat1')
            cat_list = Nugget.objects.all().filter(nuggetcat__cat__cat1=selected_cat_des)
        elif cat_level == 3:
            selected_cat_des = selected_cat.get('cat2')
            cat_list = Nugget.objects.all().filter(nuggetcat__cat__cat2=selected_cat_des)
        serializer = NuggetSerializer(cat_list, context={'request': request}, many=True)
        return Response(serializer.data)


