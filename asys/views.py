from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, AppoinmentCreSerializer, AthemaSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .int_ops import createappointment, getappointments, deleteappointment, bookappointment, getutaint, getthemen, \
    createathema, getthemasingle, createthemakommentar, getkommentare
from django.contrib.auth import authenticate, login


class UserCreate(APIView):
    """Creates the user."""
    def post(self, request, domainname, format='json'):
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
    def post(self, request, domainname, *args, **kwargs):
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


class ExampleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, domainname, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class AppointmentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, domainname, fromat=None):
        if domainname == 'localhost' or domainname == 'kariconcept.de' \
                or domainname == 'www.kariconcept.de':
            agentid = 1
        return_data = getappointments(agentid, False)
        return Response(return_data)

    def post(self, request, domainname, *args, **kwargs):
        if domainname == 'localhost' or domainname == 'kariconcept.de' \
                or domainname == 'www.kariconcept.de':
            agentid = 1
        data = request.data
        appointment_cre_data = AppoinmentCreSerializer(data=data)
        if appointment_cre_data.is_valid():
            # let that magic happen date format is YYYY-MM-DD
            beginn = data.get('d_beginn_tmsp')
            end = data.get('d_end_tmsp')
            return_message = createappointment(beginn, end)
            return_data = getappointments(agentid, False)
            return Response(return_data)

        else:
            return Response('invalid')

    def delete(self, request, domainname):
        if domainname == 'localhost' or domainname == 'kariconcept.de' \
                or domainname == 'www.kariconcept.de':
            agentid = 1
        data = request.data
        asys_id = data.get('asys_id')
        aidate_id = data.get('id')
        return_message = deleteappointment(asys_id, aidate_id)
        if return_message == 'deleted':
            return_data = getappointments(agentid, False)
            return Response(return_data)
        return Response(return_message)


class AppointmentsPublicView(APIView):
    def get(self, request, domainname, fromat=None):
        if domainname == 'localhost' or domainname == 'kariconcept.de' \
                or domainname == 'www.kariconcept.de':
            agentid = 1
        return_data = getappointments(agentid, True)
        return Response(return_data)

    def put(self, request, domainname, *args, **kwargs):
        if domainname == 'localhost' or domainname == 'kariconcept.de' \
                or domainname == 'www.kariconcept.de':
            agentid = 1
        data = request.data
        inputs = data.get('inputs')
        asys_id = data.get('asys_id')
        bookappointment(inputs, asys_id)
        return Response(True)


class UtaIntView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, domainname, fromat=None):
        if domainname == 'localhost' or domainname == 'stb-it.de' \
                or domainname == 'www.stb-it.de':
            agentid = 1
        return_data = getutaint()
        return Response(return_data)


class ThemaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, domainname, fromat=None):
        if domainname == 'localhost' or domainname == 'stb-it.de' \
                or domainname == 'www.stb-it.de':
            agentid = 1
        # get user information check if admin if admin show all themen if not only show themen from user
        userid = request.auth.user_id
        return_data = getthemen(userid)
        return Response(return_data)

    def post(self, request, domainname, *args, **kwargs):
        if domainname == 'localhost' or domainname == 'stb-it.de' \
                or domainname == 'www.stb-it.de':
            agentid = 1
        new_data = dict()
        data = request.data
        for da in data:
            new_data[da.get('name')] = da.get('value')
        ser_data = AthemaSerializer(data=new_data)
        if ser_data.is_valid():
            userid = request.auth.user_id
            # let that magic happen date format is YYYY-MM-DD
            created, return_message = createathema(new_data, userid)
            if created:
                return_data = getthemen(userid)
            else:
                return_data = return_message
            return Response(return_data)
        else:
            return Response('invalid data passed')

    def delete(self, request, domainname):
        if domainname == 'localhost' or domainname == 'stb-it.de' \
                or domainname == 'www.stb-it.de':
            agentid = 1
        data = request.data
        asys_id = data.get('asys_id')
        aidate_id = data.get('id')
        return_message = deleteappointment(asys_id, aidate_id)
        if return_message == 'deleted':
            return_data = getappointments(agentid, False)
            return Response(return_data)
        return Response(return_message)


class ThemaSingleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, domainname, thema_id, fromat=None):
        if domainname == 'localhost' or domainname == 'stb-it.de' \
                or domainname == 'www.stb-it.de':
            agentid = 1
        userid = request.auth.user_id
        return_data = getthemasingle(thema_id, userid)
        return Response(return_data)

    def post(self, request, domainname, thema_id, *args, **kwargs):
        if domainname == 'localhost' or domainname == 'stb-it.de' \
                or domainname == 'www.stb-it.de':
            agentid = 1
        new_data = dict()
        data = request.data
        for da in data:
            new_data[da.get('name')] = da.get('value')
        userid = request.auth.user_id
        new_data['athema_id'] = thema_id
        # let that magic happen date format is YYYY-MM-DD
        created, return_message = createthemakommentar(new_data, userid)
        if created:
            return_data = getkommentare(thema_id, userid)
        else:
            return_data = return_message
        return Response(return_data)




