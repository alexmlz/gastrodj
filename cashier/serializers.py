from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('pk', 'description')


class NuggetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nugget
        fields = ('pk', 'description', 'description_long', 'pic_url')


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = ('pk', 'description', 'cat0', 'cat1', 'cat2', 'cat3')
