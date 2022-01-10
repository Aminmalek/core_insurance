from django.contrib import auth
from rest_framework import permissions, status
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


from authenticate import serializers as auth_serializers
from .models import User
from Core.decorators import *


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
            return Response({"message": "error while signup"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "user signed up successfully"})


class LoginView(APIView):

    serializer_class = auth_serializers.LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            user = auth.authenticate(
                username=request.data.get('username'), password=request.data.get('password'))
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'username or password is not true'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
        This API receives plain request, logs out the user who requested
    """

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'logged out'})
        except:
            return Response({'error': 'something went wrong while logging out'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class GetUserView(APIView):
    """
        For get summary of user information
    """
    serializer_class = auth_serializers.UserSerializer
    def get(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            if user:
                serialized_data = self.serializer_class(user)
                return Response(serialized_data.data)
        except User.DoesNotExist:
            return Response({"error": "there is't any Token in data base"}, status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):
    """
        For getting user list and updating users
    """
    @type_check(("Company",))
    def get(self, request):
        type = request.query_params.get('type', None)
        if type:
            users = User.objects.filter(type=type)
        else:
            users = User.objects.all()
        users =  auth_serializers.GetUserSerializer(users, many=True)
        return Response(users.data)

    @type_check(("Company",))
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
        very simple adding money to users wallet and can see it by that user
    """
    @type_check(["Holder", "SuperHolder", "Insured"])
    def get(self, request):
        try:
            user = request.user
            return Response(user.cash)
        except:
            return Response([])

    @type_check(["Holder", "SuperHolder", "Insured"])
    def put(self, request):
        try:
            user = request.user
            data = request.data
            cash = data['cash']
            user.cash = int(cash) + user.cash
            user.save()
            return Response({"message": "user cash updated successfully"})
        except:
            return Response ({"error': 'can't update users cash "})

