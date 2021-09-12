from django.contrib import auth
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .models import User


class SignupView(APIView):
    """
        This API receives signup data, creates the user and logs in with the created user
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            user = User.objects.create_user(
                username=username, password=password)
            token = Token.objects.create(user=user)
            user.save()
            return Response({'token': token.key, 'username': username}, status=status.HTTP_201_CREATED)


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
            token = Token.objects.get(
                key=request.META.get('HTTP_AUTHORIZATION'))
            token.delete()
            return Response({'message': 'logged out'})
        except:
            content = {'error': 'something went wrong while logging out'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserView(APIView):
    """
        For set user token to header and see token is valid or not and permissions of user
    """

    def get(self, request):
        try:
            token = Token.objects.get(
                key=request.META.get('HTTP_AUTHORIZATION'))
            user = User.objects.get(auth_token=token)
            if user:
                response_data = UserSerializer(user)
                return Response(response_data.data)
            else:
                content = {"error": "user does not exist "}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        except Token.DoesNotExist:
            content = {"error": "there is not any Token in data base"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
