from authenticate.models import User
from insured.models import Insured
from payment.serializers import InsuranceConnectorSerializer
from insurance.models import Insurance
from payment.models import InsuranceConnector
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


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

    def post(self, request):
        data = request.data
        user = request.user
        if user.type == "Insured":
            user = User.objects.get(id=user.id)
            user.type = "Holder"
            user.save()
        if user.type == "Holder":
            insurance_id = data['insurance_id']
            register_form = data['register_form']
            insurance = Insurance.objects.get(id=insurance_id)
            user_cash = user.cash
            insurance_price = insurance.price

            if int(insurance_price) > int(user_cash):
                return Response({"message":"you don't have enough money to by insurance"},status=status.HTTP_400_BAD_REQUEST)
            else:
                # To deduct money from the profile after purchasing insurance
                user.cash = int(user_cash) - int(insurance_price)
                user.save()

                InsuranceConnector.objects.create(
                user=user, insurance=insurance, register_form=register_form)
                return Response({"message": "insured created successfuly"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        data = request.data
        user = request.user
        insurance_connector = InsuranceConnector.objects.get(id=id)
        if user.type == "Holder":
            user = User.objects.get(username=user.username)
            is_paid = data['is_paid']
            payment_code = data['payment_code']
            if is_paid:
                insurance_connector.is_paid = True if is_paid == "true" else False
            if payment_code:
                insurance_connector.payment_code = int(payment_code)
            insurance_connector.save()
            return Response({"message": "insurance connector updated successfuly"}, status=status.HTTP_200_OK)
                
        elif user.type == "Company":
            is_accepted_by_company = data['is_accepted_by_company']
            if is_accepted_by_company:
                insurance_connector.is_accepted_by_company = True if is_accepted_by_company == "true" else False
            insurance_connector.save()
            return Response({"message": "insurance connector updated successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
