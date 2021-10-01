from authenticate.models import User
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
            insurance = Insurance.objects.get(id=insurance_id)
            InsuranceConnector.objects.create(
                user=user, insurance=insurance)
            return Response({"message": "insured created successfuly"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        data = request.data
        user = request.user
        insurance_connector = InsuranceConnector.objects.get(id=id)
        if user.type == "Holder":
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
