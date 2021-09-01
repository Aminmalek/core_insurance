from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from . models import Insurance
from . serializers import InsuranceSerializer


class InsuranceAddView(APIView):
    def post(self, request):

        data = request.data
        name = data['name']
        description = data['description']
        new_insurance = Insurance.objects.create(
            insurance_type=name, description=description)

        if new_insurance:
            return Response({'success': f'{name} insurance created successfuly'})
        else:
            content = {'error': "can't create insurance successfuly"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def get(self, resquest):
        all_insurances = Insurance.objects.all()
        serializer = InsuranceSerializer(all_insurances, many=True)

        return Response({'available insurances': serializer.data})

    def put(self, request):
        data = request.data
        insurance_id = request.query_params.get('insurance-id')
        description = data['description']
        try:
            new_insurance = Insurance.objects.filter(
                id=insurance_id).update(description=description)
        except:
            return Response({"messege":"updating insurance was not successful"})
        return Response({"message":"insurance updated successfuly"})

    def delete(self,request):
        insurance_id = request.query_params.get('insurance-id')
        try:
            insurance = Insurance.objects.filter(id=insurance_id).delete()
            return Response({"message":"insurance deleted successfuly"})
        except:
            return Response({"message":"can't delete insurance"})