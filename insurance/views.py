from authenticate.models import User
from rest_framework.authtoken.models import Token
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
            insurance, created = Insurance.objects.get_or_create(
                name=name, description=description)
            if created:
                return Response({"message": "insurance created successfuly"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "insurance already exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        data = request.data
        user = request.user
        if user.type == 'Company':
            data = request.data
            insurance_id = data['id']
            name = data['name']
            description = data['description']
            Insurance.objects.filter(id=insurance_id).update(
                name=name, description=description)
            return Response({"message": "insurance updated successfuly"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        data = request.data
        user = request.user
        if user.type == 'Company':
            data = request.data
            insurance_id = data['id']
            Insurance.objects.filter(id=insurance_id).delete()
            return Response({"message": "insurance deleted successfuly"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
