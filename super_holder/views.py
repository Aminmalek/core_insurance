from insured.models import Insured
from rest_framework.response import Response
from rest_framework.views import APIView
from authenticate.models import User
from rest_framework import status
from .models import SuperHolder
from .serializers import SuperHolderSerializer
from authenticate.models import User


class SuperHolderView(APIView):

    def get(self, request):
        user = request.user
        if user.type == 'Company':
            superholders = SuperHolder.objects.all()
            serializer = SuperHolderSerializer(superholders, many=True)
            return Response(serializer.data)
        elif user.type == 'SuperHolder':
            superholder, created = SuperHolder.objects.get_or_create(
                user=user)
            serializer = SuperHolderSerializer(superholder)
            return Response(serializer.data)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        data = request.data
        user = request.user
        if user.type == "SuperHolder":
            username = data['username']
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']
            bank_account_number = data['bank_account_number']
            if User.objects.filter(username=username).exists() or User.objects.filter(phone=phone).exists():
                return Response({'error': 'Username or Phone number already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                            last_name=last_name, is_active=True, phone=phone, bank_account_number=bank_account_number, type='Holder')
            user.save()
            Insured.objects.create(user=user)
            SuperHolder.objects.get(
                user=request.user).supported_holders.add(user)
            return Response({"message": "holder created successfuly"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        data = request.data
        user = request.user
        if user.type == 'Company':
            user_id = data['user_id']
            user = User.objects.get(id=user_id)
        supported_holders = data['supported_holders']
        insured = SuperHolder.objects.get(user=user)
        if supported_holders:
            for id in supported_holders:
                user = User.objects.get(id=id)
                insured.supported_holders.add(user)
        insured.save()
        return Response({"message": "super holder updated successfuly"})

    def delete(self, request):
        data = request.data
        user = request.user
        if request.user.type == 'Company' or request.user.type == 'SuperHolder':
            user_id = data['user_id']
            user = User.objects.get(id=user_id)
            insured = Insured.objects.get(user=user)
            if user.type == "SuperHolder":
                try:
                    insured.supported_holders.remove(user)
                    insured.delete()
                    user.delete()
                except:
                    return Response({"message": "you can not delete this holder"}, status=status.HTTP_403_FORBIDDEN)
            else:
                insured.delete()
                user.delete()
            return Response({"message": "Holder deleted successfuly"})
