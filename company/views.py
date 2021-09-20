from django.contrib.auth.models import UserManager
from authenticate import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from authenticate.models import User
from ticket.models import Ticket
from.serializers import TicketForCompanySerializer


class CompanyTicketView(APIView):

    def get(self, request):
        """
        For view all tickets by company by status and acceptance of vendor
        """
        data = request.data
        # I add [6:] because Token set to header like this Token e6r5g4e6r54ge
        token = Token.objects.get(
            key=request.META.get('HTTP_AUTHORIZATION')[6:])
        user = User.objects.get(auth_token=token)

        if user.type == 'Company':
            ticket = Ticket.objects.all()
            serializer = TicketForCompanySerializer(ticket, many=True)
            return Response(serializer.data)
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        """
            This method is for posting username and activation status of vendor and active
            or deactive him or her
        """
        data = request.data
        # I add [6:] because Token set to header like this Token e6r5g4e6r54ge
        token = Token.objects.get(
            key=request.META.get('HTTP_AUTHORIZATION')[6:])
        user = User.objects.get(auth_token=token)

        if user.type == 'Company':
            ticket_company_status = bool(data['status'])
            ticket_id = data['ticket_id']
            Ticket.objects.filter(id=ticket_id).update(
                is_accepted_by_company=ticket_company_status)
            return Response({"message": "Ticket status updated successfuly by company"})
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class VendorActivatedView(APIView):

    def post(self, request):
        """
            Company user can post username of vendor and see the activation status
        """
        data = request.data
        # I add [6:] because Token set to header like this Token e6r5g4e6r54ge
        token = Token.objects.get(
            key=request.META.get('HTTP_AUTHORIZATION')[6:])
        user = User.objects.get(auth_token=token)

        if user.type == 'Company':
            data = request.data
            vendor_username = data['vendor_username']
            vendor = User.objects.get(username=vendor_username)
            return Response({"user activated": vendor.is_active})
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        """
            Company user can active or deactive the user by send username and new status 
        """
        data = request.data
        # I add [6:] because Token set to header like this Token e6r5g4e6r54ge
        token = Token.objects.get(
            key=request.META.get('HTTP_AUTHORIZATION')[6:])
        user = User.objects.get(auth_token=token)

        if user.type == 'Company':
            data = request.data
            vendor_username = data['vendor_username']
            vendor_activation_status = data['vendor_activation_status']

            try:
                vendor = User.objects.get(username=vendor_username)
                vendor.is_active = vendor_activation_status
                vendor.save()
            except:
                content = {
                    "message": "There is no one with this username in the database"}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "vendor activation status changed successfuly"})
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
