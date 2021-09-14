from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from authenticate.models import User
from ticket.models import Ticket
from.serializers import TicketForCompanySerializer


class CompanyTicketView(APIView):

    def get(self, request):

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

        data = request.data
        # I add [6:] because Token set to header like this Token e6r5g4e6r54ge
        token = Token.objects.get(
            key=request.META.get('HTTP_AUTHORIZATION')[6:])
        user = User.objects.get(auth_token=token)

        if user.type == 'Company':
            ticket_company_status = bool(data['status'])
            ticket_id = data['ticket_id']
            ticket_for_update = Ticket.objects.filter(id=ticket_id).update(
                is_accepted_by_company=ticket_company_status)
            return Response({"message": "Ticket status updated successfuly by company"})
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class VendorActivatedView(APIView):

    def post(self, request):

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

        data = request.data
        # I add [6:] because Token set to header like this Token e6r5g4e6r54ge
        token = Token.objects.get(
            key=request.META.get('HTTP_AUTHORIZATION')[6:])
        user = User.objects.get(auth_token=token)

        if user.type == 'Company':
            data = request.data
            vendor_username = data['vendor_username']
            vendor_activation_status = data['vendor_activation_status']
            User.objects.filter(username=vendor_username).update(
                is_active=vendor_activation_status)
            # For see the vendor status after activation
            #vendor = User.objects.get(username=vendor_username)
            return Response({"message": "vendor activation status changed successfuly"})
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
