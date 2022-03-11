from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import AiSysDate



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


class AppoinmentCreSerializer(serializers.ModelSerializer):
    d_end_tmsp = serializers.CharField(max_length=10)
    d_beginn_tmsp = serializers.CharField(max_length=10)

    class Meta:
        model = AiSysDate
        fields = ('d_end_tmsp', 'd_beginn_tmsp')
