from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('pk', 'description')


class NuggetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nugget
        fields = ('pk', 'description', 'description_long', 'pic_url', 'addonflag', 'description_long', 'active',
                  'einzelpreis', 'einheit', 'menge', 'mt', 'optioncat')


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = ('pk', 'description', 'cat0', 'cat1', 'cat2', 'cat3')


class OptionCatSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionCat
        fields = ('pk', 'description')


class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ('pk', 'description', 'nugget', 'menge', 'einzelpreis', 'value', 'einheit', 'group',
                  'addonflag', 'folg', 'lastchanged', 'mt')


class FolgSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folg
        fields = ('pk', 'description', 'pp', 'pair', 'status', 'method', 'paymentdetails', 'lastchanged', 'mt')
