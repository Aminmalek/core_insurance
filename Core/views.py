from rest_framework.views import APIView
from rest_framework.response import Response
from . decorators import *


class TestView(APIView):

    @is_insured
    @is_company
    def get(self,request):
        return Response({"this is for test get"})

    
    @is_company
    def post(self,request):
        return Response({"this is for test post"})

    @is_company_or_insured
    def delete(self,request):
        return Response({"this is for test delete"})