from authenticate.models import User
from insured.models import Insured
from payment.serializers import InsuranceConnectorSerializer
from insurance.models import Insurance
from payment.models import InsuranceConnector
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Core.decorators import is_holder_insured

class InsuranceConnectorView(APIView):
    def get(self, request):
        user = request.user
        if user.type == "Company":
            insurance_connector = InsuranceConnector.objects.all()
            insurance_connector = InsuranceConnectorSerializer(
                insurance_connector, many=True)
            return Response(insurance_connector.data)
        elif user.type == "Holder" or user.type == "SuperHolder":
            insurance_connector = InsuranceConnector.objects.filter(
                user=user)
            insurance_connector = InsuranceConnectorSerializer(
                insurance_connector, many=True)
            return Response(insurance_connector.data)
        elif user.type == "Insured":
            parent = Insured.objects.get(supported_insureds=user)
            insurance_connector = InsuranceConnector.objects.filter(
                user=parent.user)
            insurance_connector = InsuranceConnectorSerializer(
                insurance_connector, many=True)
            return Response(insurance_connector.data)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    @is_holder_insured
    def post(self, request):
        data = request.data
        user=request.user
        insurance_id = data['insurance_id']
        register_form = data['register_form']
        insurance = Insurance.objects.get(id=insurance_id)
        InsuranceConnector.objects.create(
            user=user, insurance=insurance, register_form=register_form)
        return Response({"message": "insured created successfuly"}, status=status.HTTP_201_CREATED)

    
    def put(self, request, id):
        data = request.data
        user = request.user
        insurance_connector = InsuranceConnector.objects.get(id=id)
        
        if user.type == "Holder" or user.type == "Insured":
            user = User.objects.get(id=user.id)
            insurance_price = insurance_connector.insurance.price
            user_cash = user.cash

            if int(user_cash) > int(insurance_price) :
                payment_code = data['payment_code']
                user.cash = int(user_cash) - int(insurance_price)
                if user.type == "Insured":
                    user.type = "Holder"
                insurance_connector.is_paid = True
                user.save()
                insurance_connector.save()
                #insurance_connector.payment_code = int(payment_code)
                if payment_code and insurance_connector.is_paid == True:
                    return Response({"message": "insurance connector updated successfuly"})
                else:
                    return Response({"error": "insurance connector updated successfuly"},status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({"message":"you don't have enough money to by insurance"},status=status.HTTP_400_BAD_REQUEST)

        elif user.type == "Company":
            is_accepted_by_company = data['is_accepted_by_company']
            if is_accepted_by_company:
                insurance_connector.is_accepted_by_company = True if is_accepted_by_company == "true" else False
            insurance_connector.save()
            return Response({"message": "insurance connector updated successfuly"})
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
