from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from insured.models import Insured
from authenticate.models import User
from Core.decorators import type_check, type_confirmation
from .serializers import InsuredSerializer


class InsuredView(APIView):

    @type_check(("Company", "Insured", "Holder"))
    def get(self, request):
        user = request.user

        if type_confirmation(user.type, ("Company",)):
            insureds = Insured.objects.all()
            serializer = InsuredSerializer(insureds, many=True)
            return Response(serializer.data)
        elif type_confirmation(user.type, ("Holder", "Insured")):
            insured, created = Insured.objects.get_or_create(user=user)
            serializer = InsuredSerializer(insured)
            return Response(serializer.data)

    @type_check(("Holder",))
    def post(self, request):
        data = request.data
        user = request.user
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        phone = data['phone']
        bank_account_number = data['bank_account_number']

        if User.objects.filter(username=username).exists() or User.objects.filter(phone=phone).exists():
            return Response({'error': 'Username or Phone number already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            supported_user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                      last_name=last_name, is_active=True, phone=phone, bank_account_number=bank_account_number, type=5)
            Insured.objects.create(user=supported_user)
            holder = Insured.objects.get(user=user)
            holder.supported_insureds.add(supported_user)
            return Response({"message": "insured created successfuly"}, status=status.HTTP_201_CREATED)

    @type_check(("SuperHolder", "Holder"))
    def put(self, request, id):
        data = request.data
        user = request.user
        supported_insureds = data['supported_insureds']
        holder = Insured.objects.get(user=user)
        if supported_insureds:
            supported_user = User.objects.get(id=supported_insureds)
            holder.supported_insureds.add(supported_user)
        holder.save()
        return Response({"message": "insured updated successfuly"})

    @type_check(("Company", "Holder"))
    def delete(self, request, id):
        user = request.user
        if type_confirmation(user.type, ("Company",)):
            Insured.objects.filter(user=id).delete()
            User.objects.filter(id=id).update(is_active=False)
            return Response({"message": "insured deleted successfuly"})
        else:
            holder = Insured.objects.get(user=user)
            insured_user = User.objects.get(id=id)
            holder.supported_insureds.remove(insured_user)
            User.objects.filter(id=id).update(is_active=False)
            return Response({"message": "insured deleted successfuly"})
