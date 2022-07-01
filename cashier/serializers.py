from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('pk', 'description')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class NuggetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nugget
        fields = ('pk', 'description', 'description_long', 'pic_url', 'addonflag', 'description_long', 'active',
                  'einzelpreis', 'einheit', 'menge', 'mt', 'optioncat', 'post')


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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=32,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
