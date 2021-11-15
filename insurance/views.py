from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Insurance, Coverage
from .serializers import InsuranceSerializer
from Core.decorators import type_check
import json
import uuid


class InsuranceView(APIView):
    """
        This api is used to handle full crud operations on insurance
    """

    def guid_generator(self, object):
        obj = json.loads(object)
        for i in obj:
            if 'id' not in i:
                i['id'] = str(uuid.uuid4())
        return obj

    @type_check(("Company", "Holder", "Insured", "SuperHolder", 'CompanyAdmin',))
    def get(self, request, id=None):
        if id:
            try:
                insurance = Insurance.objects.get(id=id)
                serializer = InsuranceSerializer(insurance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({"message": "insurance doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            insurance = Insurance.objects.all()
            serializer = InsuranceSerializer(insurance, many=True)
            return Response(serializer.data)

    @type_check(["Company", "CompanyAdmin"])
    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 1:
            name = data['name']
            description = data['description']
            price = data['price']
            coverage = json.loads((data['coverage']))
            register_form = self.guid_generator(data['register_form'])
            if Insurance.objects.filter(name=name).exists():
                return Response({"message": "insurance already exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                insurance = Insurance.objects.create(
                    name=name, description=description, price=price, register_form=register_form)

            for objects in coverage:
                cover = Coverage.objects.create(
                    name=objects['name'], claim_form=objects['claim_form'], capacity=objects['capacity'])
                insurance.coverage.add(cover)

            return Response({"message": "insurance created successfuly"}, status=status.HTTP_201_CREATED)

    @type_check(["Company", "CompanyAdmin"])
    def put(self, request, id):
        data = request.data
        name = data['name']
        description = data['description']
        price = data['price']
        register_form = self.guid_generator(data['register_form'])

        insurance = Insurance.objects.filter(id=id)
        if insurance:
            insurance.update(
                name=name, description=description, price=price, register_form=register_form)
            return Response({"message": "insurance updated successfuly"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": "insurance doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

    @type_check(["Company", "CompanyAdmin"])
    def delete(self, request, id):
        insurance = Insurance.objects.filter(id=id)
        if insurance:
            Insurance.objects.get(id=id).delete()
            return Response({"message": "insurance deleted successfuly"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": "insurance doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
