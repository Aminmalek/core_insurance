from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Insurance
from .serializers import InsuranceSerializer


class InsuranceView(APIView):
    """
        This api is used to handle full crud operations on insurance
    """

    def get(self, resquest):
        all_insurances = Insurance.objects.all()
        serializer = InsuranceSerializer(all_insurances, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 'Company':
            name = data['name']
            description = data['description']
            type = data['type']
            price = data['price']
            if Insurance.objects.filter(name=name).exists():
                return Response({"message": "insurance already exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Insurance.objects.create(
                    name=name, description=description, type=type, price=price)
            return Response({"message": "insurance created successfuly"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        data = request.data
        user = request.user
        if user.type == 'Company':
            data = request.data
            name = data['name']
            description = data['description']
            type = data['type']
            price = data['price']
            insurance = Insurance.objects.filter(id=id)
            if insurance:
                insurance.update(
                    name=name, description=description, type=type, price=price)
                return Response({"message": "insurance updated successfuly"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "insurance doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id):
        user = request.user
        if user.type == 'Company':
            insurance = Insurance.objects.filter(id=id)
            if insurance:
                Insurance.objects.get(id=id).delete()
                return Response({"message": "insurance deleted successfuly"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "insurance doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
