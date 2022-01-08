import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Core.decorators import type_check
from .models import Insurance, Coverage
from .serializers import InsuranceSerializer


class InsuranceView(APIView):
    """
        This api is used to handle full crud operations on insurance
    """
    def uuid_generator(self, object):

        for item in object:
            if 'id' not in item:
                item['id'] = str(uuid.uuid4())
        return object

    @type_check(("Company", "Holder", "Insured", "SuperHolder", 'CompanyAdmin'))
    def get(self, request, id=None):
        user = request.user
        if id:
            insurance = Insurance.objects.get(id=id)
            serializer = InsuranceSerializer(insurance)
            return Response(serializer.data)
        else:
            insurance = Insurance.objects.all()
            serializer = InsuranceSerializer(insurance, many=True)
            return Response(serializer.data)

    @type_check(("Company", "CompanyAdmin"))
    def post(self, request):
        data = request.data
        name = data['name']
        description = data['description']
        price = data['price']
        coverages = data['coverage']
        register_form = self.uuid_generator(data['register_form'])
        insurance = Insurance.objects.create(
            name=name, description=description, price=price, register_form=register_form)
        for coverage in coverages:
            claim_form = self.uuid_generator(coverage["claim_form"])
            coverage_instance = Coverage.objects.create(
                name=coverage['name'], claim_form=claim_form, capacity=coverage['capacity'])
            insurance.coverage.add(coverage_instance)
        return Response({"message": "insurance created successfuly"}, status=status.HTTP_201_CREATED)

    @type_check(["Company", "CompanyAdmin"])
    def put(self, request, id):
        data = request.data
        name = data['name']
        description = data['description']
        price = data['price']
        coverage = data['coverage']
        register_form = self.uuid_generator(data['register_form'])

        if Insurance.objects.filter(id=id).exists():
            insurance = Insurance.objects.get(id=id)
            if name:
                insurance.name
            if description:
                insurance.description = description
            if price:
                insurance.price = price
            if register_form:
                insurance.register_form = register_form
            if coverage:
                insurance.coverage.clear()
                for objects in coverage:
                    claim_form = self.uuid_generator(objects["claim_form"])
                    cover = Coverage.objects.create(
                        name=objects['name'], claim_form=claim_form, capacity=objects['capacity'])
                    insurance.coverage.add(cover)
            insurance.save()
            return Response({"message": "insurance updated successfuly"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"error": "insurance doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    @type_check(["Company", "CompanyAdmin"])
    def delete(self, request, id):
        if Insurance.objects.filter(id=id).exists():
            Insurance.objects.get(id=id).delete()
            return Response({"message": "insurance deleted successfuly"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": "insurance doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
