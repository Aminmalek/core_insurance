from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.views import APIView
from payment.models import InsuranceConnector
from authenticate.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group


class GetGroupView(APIView):

    def get(self, request):
        token_header=request.META.get('HTTP_AUTHORIZATION')
        # Token in auth header set like this : Token 6354d54ffef4vfsfrgv5...
        token_key = token_header[6:]
        token = Token.objects.get(key=token_key)
        user = User.objects.get(auth_token=token)
        group_of_user = Group.objects.filter(user=user)
        
        return Response({"groups of user":group_of_user})

class NewInsuranceView(APIView):

    def post(self, request):
        '''
        data = request.data
        insurance_id = data['insurance_id']
        #this data must post from bank
        payment_status = data['payment_status']

        connector = InsuranceConnector.objects.create(insurance=insurance_id,)
        content = {"success":"insurance connectore is successful"}
        return Response(content)
        '''
        pass
