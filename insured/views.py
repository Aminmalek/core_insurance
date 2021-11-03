from rest_framework.response import Response
from rest_framework.views import APIView
from authenticate.models import User
from rest_framework import status
from insured.models import Insured
from . serializers import InsuredSerializer
from authenticate.models import User
from Core.decorators import *

permissions_dic = {"Company": 1, "Vendor": 2,
                               "SuperHolder": 3, "Holder": 4, "Insured": 5}

class InsuredView(APIView):

    @type_check(["Company","Insured","Holder"])
    def get(self, request):
        user = request.user
        if user.type == 1:
            insureds = Insured.objects.all()
            serializer = InsuredSerializer(insureds, many=True)
            return Response(serializer.data)
        else : 
            user.type == 5 or user.type == 4
            insured, created = Insured.objects.get_or_create(user=user)
            serializer = InsuredSerializer(insured)
            return Response(serializer.data)

    @type_check(["Holder"])
    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 4:

            username = data['username']
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']
            bank_account_number = data['bank_account_number']

            if User.objects.filter(username=username).exists() or User.objects.filter(phone=phone).exists():
                return Response({'error': 'Username or Phone number already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            user = User.objects.create_user(username=username,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name,
                                            is_active=True,
                                            phone=phone,
                                            bank_account_number=bank_account_number,
                                            type=5)
            user.save()
            Insured.objects.create(user=user)
            #return Response({"message": "insured created successfuly"}, status=status.HTTP_201_CREATED)
            # Commenting this part makes tests pass
            
            if request.user.type == "Holder":
                
                insured = Insured.objects.get(user=request.user)
                insured.supported_insureds.add(user)
            return Response({"message": "insured created successfuly"}, status=status.HTTP_201_CREATED)
            
    def put(self, request, id):
        data = request.data
        user = request.user
        supported_insureds = data['supported_insureds']
        insured = Insured.objects.get(user=user)
        if supported_insureds:
            user = User.objects.get(id=supported_insureds)
            insured.supported_insureds.add(user)
        insured.save()
        return Response({"message": "insured updated successfuly"})
        
    @type_check(["Company","Holder"])
    def delete(self, request, id):
        user = request.user
        user_id = User.objects.get(id=id)
        insured = Insured.objects.get(user=user_id)
        if user.type == 1:
            user.delete()
            insured.delete()
        elif user.type == 4:
            try:
                insured.supported_insureds.remove(user)
                insured.delete()
                user.delete()
            except:
                return Response({"message": "you can not delete this insured"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "insured deleted successfuly"})
