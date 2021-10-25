from django.db.models.query_utils import RegisterLookupMixin
from authenticate.models import User
from insured.models import Insured
from payment.serializers import InsuranceConnectorSerializer
from insurance.models import Insurance
from payment.models import InsuranceConnector
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Core.decorators import is_company, is_holder_insured

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
        user = User.objects.get(id=user.id)
        if int(user.cash) >= int(insurance.price) :
            user.cash = int(user.cash) - int(insurance.price)
            InsuranceConnector.objects.create(
            user=user, insurance=insurance, register_form=register_form, is_paid=True)
            user.type = "Holder"
            user.save()
        else:
            return Response({"error":"you have not enough money to buy insurance"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "insurance purchased successfuly"}, status=status.HTTP_201_CREATED)

    @is_company
    def put(self, request, id):
        data = request.data
        insurance_connector = InsuranceConnector.objects.get(id=id)
        is_accepted_by_company = data['is_accepted_by_company']
        if is_accepted_by_company is not None:
            insurance_connector.is_accepted_by_company = True if is_accepted_by_company == "true" else False
        else:
            return Response({"error":"please enter correct data"},status=status.HTTP_400_BAD_REQUEST)
        insurance_connector.save()
        return Response({"message": "insurance connector updated successfuly"})
    