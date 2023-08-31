from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import UniqueValidator
# from django.core.exceptions import ValidationError
UserModel = get_user_model()
# from rest_framework.validators import UniqueValidator

from .models import *


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(email=clean_data['email'],
                                                 username=clean_data['username'],
                                                 password=clean_data['password'])
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    ##

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['username'], password=clean_data['password'])
        if not user:
            user_ex = User.objects.get(username=clean_data['username'])
            if user_ex:
                return 'invalid password'
            else:
                return 'user not found'
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model: UserModel
        fields = ('email', 'username')


class UserSerializer1(serializers.ModelSerializer):
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


class JournalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Journal
        fields = ('id', 'content', 'cre_date', 'subject', 'user')
