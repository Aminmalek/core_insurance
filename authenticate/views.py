from django.contrib.auth.models import User, Permission
from django.contrib import auth
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer


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


'''
class CheckAuthenticatedView(APIView):
    """
       token set on header and check valid or not 
    """
'''


class LoginView(APIView):
    """
       In this view cleint must set token in header and post user and pass
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
            return Response({'error': 'user is not auhtenticated'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
        This APi receives plain request, logs out the user who requested
    """

    def post(self, request):
        try:
            auth.logout(request)
            return Response({'success': 'logged out'})
        except:
            content = {'error': 'something went wrong while logging out'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserView(APIView):
    # full name and access
    # response full name and access
    # token is not valid
    #

    permission_classes = (permissions.AllowAny,)

    def get(self, request):

        try:
            token = Token.objects.get(
                key=request.META.get('HTTP_AUTHORIZATION'))
            user = User.objects.get(auth_token=token)

            if user:
                token_is_valid = True
                user_permisoins = user.get_user_permissions()
                response_data = UserSerializer(user)

                return Response(
                    {"user": response_data.data, "permisions": user_permisoins,
                     "token_is_valid": token_is_valid})
            else:
                content = {"error": "user does not exist "}
                return Response(content,status=status.HTTP_401_UNAUTHORIZED)

        except Token.DoesNotExist:
            content = {"error": "there is not any Token in data base"}
            return Response(content,status=status.HTTP_404_NOT_FOUND)
