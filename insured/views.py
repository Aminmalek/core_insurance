from insurance.models import Insurance
from rest_framework.response import Response
from rest_framework.views import APIView
from authenticate.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from insured.models import Insured
from . serializers import InsuredSerializer
from authenticate.models import User


class InsuredView(APIView):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')[6:]
        token = Token.objects.get(key=token)
        user = User.objects.get(auth_token=token)
        if user.type == 'Company':
            insureds = Insured.objects.all()
            serializer = InsuredSerializer(insureds, many=True)
            return Response(serializer.data)
        else:
            insured = Insured.objects.get(user=user)
            serializer = InsuredSerializer(insured)
            return Response(serializer.data)

    def post(self, request):
        data = request.data
        user_id = data['user_id']
        insurance_id = data['insurance_id']
        user = User.objects.get(id=user_id)
        Insured.objects.create(user=user, insurance=insurance_id)
        return Response({"message": "insured created successfuly"}, status=status.HTTP_201_CREATED)

    def put(self, request):
        data = request.data
        token = request.META.get('HTTP_AUTHORIZATION')[6:]
        token = Token.objects.get(key=token)
        user = User.objects.get(auth_token=token)
        if user.type == 'Company':
            user_id = data['user_id']
            user = User.objects.get(id=user_id)
        is_holder = bool(data['is_holder'])
        supported_insureds = data['supported_insureds']
        bank_account_number = data['bank_account_number']
        insured = Insured.objects.get(user=user)
        if is_holder:
            insured.is_holder = is_holder
        if supported_insureds:
            for id in supported_insureds:
                user = User.objects.get(id=id)
                new_insured = Insured.objects.get(user=user)
                insured.supported_insureds.add(new_insured)
        if bank_account_number:
            insured.bank_account_number = bank_account_number
        insured.save()
        return Response({"message": "insured updated successfuly"})

    def delete(self, request):
        data = request.data
        token = request.META.get('HTTP_AUTHORIZATION')[6:]
        token = Token.objects.get(key=token)
        user = User.objects.get(auth_token=token)
        if user.type == 'Company':
            user_id = data['user_id']
            user = User.objects.get(id=user_id)
        insured = Insured.objects.get(user=user)
        insured.delete()
