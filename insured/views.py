from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from payment.models import InsuranceConnector
from authenticate.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from rest_framework import status
from insured.models import Insured
from . serializers import InsuredSerializer
from authenticate.models import User


class GetGroupView(APIView):

    def get(self, request):
        token_header = request.META.get('HTTP_AUTHORIZATION')
        # Token in auth header set like this : Token 6354d54ffef4vfsfrgv5...
        token_key = token_header[6:]
        token = Token.objects.get(key=token_key)
        user = User.objects.get(auth_token=token)
        group_of_user = Group.objects.filter(user=user)

        return Response({"groups of user": group_of_user})


class NewInsuranceView(APIView):

    def post(self, request):
        '''
        data = request.data
        insurance_id = data['insurance_id']
        #this data must post from bank
        payment_status = data['payment_status']

        connector = InsuranceConnector.objects.create(insurance=insurance_id,)
        content = {"success":"insurance connectore is successful"}
        return Response(content)
        '''
        pass


class AddInsuredView(APIView):

    def post(self, request):

        data = request.data
        # username is code melli
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']

        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            user = User.objects.create_user(
                username=username, password=password,
                first_name=first_name, last_name=last_name)

            # Making new insured
            insured = Insured.objects.create(user=user,)
            token = Token.objects.create(user=user)
            user.save()
            return Response({'username': username, 'insured': 'created', 'token': token.key, },
                            status=status.HTTP_201_CREATED)

    def get(self, request):

        all = Insured.objects.all()
        serializer = InsuredSerializer(all, many=True)
        return Response({"All Insureds": serializer.data})

    # There is a poblem here one holder only can have 1 insured
    def put(self, request):
        # After making insured user will updated to holder or insured
        data = request.data
        user_id = data['user_id']
        is_holer = data['is_holder']
        supported_insureds = data['supported_insureds']

        insured = Insured.objects.filter(
            id=user_id).update(is_holder=is_holer, supported_insureds=supported_insureds)

        return Response({"message": "insured updated successfuly"})


class GetRemoveInsuredView(APIView):

    def get(self, request):

        token_header = request.META.get('HTTP_AUTHORIZATION')
        # Token in auth header set like this : Token 6354d54ffef4vfsfrgv5...
        token_key = token_header[6:]
        token = Token.objects.get(key=token_key)
        user = User.objects.get(auth_token=token)
        holder = Insured.objects.get(user=user.id)

        serializer = InsuredSerializer(holder)
        insured = Insured.objects.filter(
            id=serializer.data['supported_insureds'])

        insured_serializer = InsuredSerializer(insured,many=True)

        return Response({"supported insureds id are:": serializer.data['supported_insureds'],
        "insured":insured_serializer.data})

    def delete(self, request):

        token_header = request.META.get('HTTP_AUTHORIZATION')
        # Token in auth header set like this : Token 6354d54ffef4vfsfrgv5...
        token_key = token_header[6:]
        token = Token.objects.get(key=token_key)
        user = User.objects.get(auth_token=token)
        holder = Insured.objects.get(user=user.id)
