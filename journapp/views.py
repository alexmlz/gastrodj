# from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework import permissions, status

from django.contrib.auth import get_user_model, login, logout
# Create your views here.


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request ):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user:
                return Response(model_to_dict(user), status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            if isinstance(user, str):
                return Response(user, status=status.HTTP_400_BAD_REQUEST)
            else:
                login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    def post(self, request, ):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes(permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication, )

    def get(self, request, ):
        serializer = UserSerializer1(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class UsersView(APIView):
    permission_classes(permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication, )

    def get(self, request, ):
        # serializer = UserSerializer1(request.user)
        if request.user.username == 'alex':
            users = User.objects.all().values()
            return Response(users, status=status.HTTP_200_OK)
        else:
            return Response('geh mal wandern', status=status.HTTP_404_NOT_FOUND)


class UserCreate(APIView):
    """Creates the user."""
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'email': user.email,
        })


@api_view(['GET', 'POST', 'DELETE'])
def journal_list(request, ):
    permission_classes(permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication, )
    # mt_id = _getmt()
    user_id = request.user.id
    #if user_id is None:#
    #    user_id = 1
    if request.method == 'GET':
        journal_list = Journal.objects.filter(user_id=user_id)
        serializer = JournalSerializer(journal_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)
    elif request.method == 'POST':
        new_data = {}
        data = request.data
        for da in data:
            new_data[da] = data[da]
        new_data['user'] = user_id
        serializer = JournalSerializer(data=new_data)
        if serializer.is_valid():
            new_journal = serializer.save()
            return Response(model_to_dict(new_journal), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def journal(request, journal_id):
    # mt_id = _getmt()
    permission_classes(permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication, )
    user_id = request.user.id
    #if user_id is None:#
    #    user_id = 1
    if request.method == 'GET':
        journal = Journal.objects.get(id=journal_id, user_id=user_id)
        serializer = JournalSerializer(journal, context={'request': request}, many=False)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        journal = Journal.objects.filter(id=journal_id, user_id=user_id)
        journal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        data = request.data
        serializer = JournalSerializer(data=data)
        if serializer.is_valid():
            Journal.objects.filter(id=journal_id, user_id=user_id).update(**data)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def question_list(request, ):
    permission_classes(permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication, )
    # mt_id = _getmt()
    user_id = request.user.id
    #if user_id is None:#
    #    user_id = 1
    if request.method == 'GET':
        question_list = Question.objects.all()
        serializer = QuestionSerializer(question_list, context={'request': request}, many=True)
        return Response(serializer.data)
        # return JsonResponse(list(product_list), safe=False)


@api_view(['GET'])
def question(request, ):
    # mt_id = _getmt()
    permission_classes(permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication, )
    user_id = request.user.id
    #if user_id is None:#
    #    user_id = 1
    if request.method == 'GET':
        question = Question.objects.order_by('?')[0]
        serializer = QuestionSerializer(question, context={'request': request}, many=False)
        return Response(serializer.data)
