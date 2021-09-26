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
        user = request.user
        if user.type == 'Company':
            insureds = Insured.objects.all()
            serializer = InsuredSerializer(insureds, many=True)
            return Response(serializer.data)
        elif user.type == 'Insured' or user.type == "Holder":
            insured, created = Insured.objects.get_or_create(user=user)
            serializer = InsuredSerializer(insured)
            return Response(serializer.data)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        data = request.data
        user = request.user
        if user.type == "Holder":
            username = data['username']
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']
            if User.objects.filter(username=username).exists() or User.objects.filter(phone=phone).exists():
                return Response({'error': 'Username or Phone number already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name, is_active=True, phone=phone, type='Insured')
            user.save()
            Insured.objects.create(user=user)
            if request.user.type == "Holder":
                Insured.objects.get(
                    user=request.user).supported_insureds.add(user)
            return Response({"message": "insured created successfuly"}, status=status.HTTP_201_CREATED)

    def put(self, request):
        data = request.data
        user = request.user
        if user.type == 'Company':
            user_id = data['user_id']
            user = User.objects.get(id=user_id)
        supported_insureds = data['supported_insureds']
        bank_account_number = data['bank_account_number']
        insured = Insured.objects.get(user=user)
        if supported_insureds:
            for id in supported_insureds:
                user = User.objects.get(id=id)
                insured.supported_insureds.add(user)
        if bank_account_number:
            insured.bank_account_number = bank_account_number
        insured.save()
        return Response({"message": "insured updated successfuly"})

    def delete(self, request):
        data = request.data
        user = request.user
        user_id = data['user_id']
        user = User.objects.get(id=user_id)
        insured = Insured.objects.get(user=user)
        if user.type == 'Company':
            user.delete()
            insured.delete()
        elif user.type == "Holder":
            try:
                insured.supported_insureds.remove(user)
                insured.delete()
                user.delete()
            except:
                return Response({"message": "you can not delete this insured"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "insured deleted successfuly"})
