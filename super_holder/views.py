from insured.models import Insured
from rest_framework.response import Response
from rest_framework.views import APIView
from authenticate.models import User
from rest_framework import status
from .models import SuperHolder
from .serializers import SuperHolderSerializer
from authenticate.models import User
from Core.decorators import type_check, type_confirmation


class SuperHolderView(APIView):

    @type_check(("Company", "SuperHolder"))
    def get(self, request):
        user = request.user
        if type_confirmation(user.type, ("Company",)):
            superholders = SuperHolder.objects.all()
            serializer = SuperHolderSerializer(superholders, many=True)
            return Response(serializer.data)
        elif type_confirmation(user.type, ("SuperHolder",)):
            superholder, created = SuperHolder.objects.get_or_create(
                user=user)
            serializer = SuperHolderSerializer(superholder)
            return Response(serializer.data)

    @type_check(("SuperHolder",))
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        phone = data['phone']
        bank_account_number = data['bank_account_number']
        if User.objects.filter(username=username).exists() or User.objects.filter(phone=phone).exists():
            return Response({'error': 'Username or Phone number already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                        last_name=last_name, is_active=True, phone=phone, bank_account_number=bank_account_number, type=4)
        user.save()
        Insured.objects.create(user=user)
        SuperHolder.objects.get(
            user=request.user).supported_holders.add(user)
        return Response({"message": "holder created successfuly"}, status=status.HTTP_201_CREATED)

    @type_check(("SuperHolder",))
    def put(self, request):

        data = request.data
        user = request.user
        supported_holders = data['supported_holders']
        super_holder = SuperHolder.objects.get(user=user)
        user = User.objects.get(id=supported_holders)
        super_holder.supported_holders.add(user)
        super_holder.save()
        return Response({"message": "super holder updated successfuly"})

    @type_check(("Company", "SuperHolder", 'Holder'))
    def delete(self, request, id):
        user = request.user
        if type_confirmation(user.type, ("SuperHolder","Company")):
            insured_user = User.objects.get(id=id)
            if type_confirmation(insured_user.type, ("Holder",)):
                if Insured.objects.filter(user=insured_user).exists():
                    insured = Insured.objects.get(user=insured_user)
                    supported_holder = SuperHolder.objects.get(user=user)
                    if type_confirmation(user.type, ("SuperHolder",)):
                        try:
                            supported_holder.supported_holders.remove(
                                insured_user)
                            insured.delete()
                            insured_user.delete()
                        except:
                            return Response({"message": "you can only delete your supported holders"}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        insured.delete()
                        user.delete()
                    return Response({"message": "Holder deleted successfuly"})
                else:
                    return Response({"message": "Holder does not exist"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message": "you can only delete holders"}, status=status.HTTP_403_FORBIDDEN)
