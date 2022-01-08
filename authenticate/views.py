from django.contrib import auth
from rest_framework import permissions, status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from authenticate import serializers as auth_serializers
from .models import User
from Core.decorators import *
from rest_framework import exceptions


class SignupView(APIView):
    """
        This API receives signup data, creates the user and logs in with the created user
    """
    serializer_class = auth_serializers.SignupSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()   
        except:
            return  Response({"message":"error while signup"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"user signed up successfully"})

class LoginView(APIView):
    """
       View for login user and get generate user
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            content = {'error': 'Username or Password is not true'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
        This API receives plain request, logs out the user who requested
    """

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'logged out'})
        except:
            content = {'error': 'something went wrong while logging out'}
            return Response(content, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class GetUserView(APIView):
    """
        For set user token to header and see token is valid or not and permissions of user
    """

    def get(self, request):
        try:
            user = request.user
            if user:
                response_data = UserSerializer(user)
                return Response(response_data.data)
            else:
                content = {"error": "user does not exist "}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        except Token.DoesNotExist:
            content = {"error": "there is not any Token in data base"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):
    """
        For getting user list and updating users
    """
    @type_check(["Company"])
    def get(self, request):
        type = request.query_params.get('type', None)
        if type:
            users = User.objects.filter(type=type)
        else:
            users = User.objects.all()
        users = UserSerializer(users, many=True)

        return Response(users.data)

    @type_check(["Company"])
    def put(self, request, id):
        data = request.data
        is_active = data['is_active']
        type = data['type']
        user = User.objects.get(id=id)
        if is_active is not None:
            user.is_active = is_active
        if type:
            user.type = type
        user.save()
        return Response({"message": "user updated successfully"})


class FinancialManagementView(APIView):
    """
        adding money to users wallet and can see it by that user
    """
    @type_check(["Holder", "SuperHolder", "Insured"])
    def get(self, request):
        user = request.user
        return Response(user.cash)

    @type_check(["Holder", "SuperHolder", "Insured"])
    def put(self, request):
        user = request.user
        data = request.data
        cash = data['cash']
        user.cash = int(cash) + user.cash
        user.save()
        return Response({"message": "user cash updated successfully"})
