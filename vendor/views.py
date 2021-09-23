from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from authenticate.models import User
from ticket.models import Ticket
from .serializers import TicketForVendorSerializer


class TicketByVendorView(APIView):

    def get(self, request):
        """
            For view all tickets by vendor
        """
        data = request.data
        user = request.user
        if user.type == 'Vendor':
            ticket = Ticket.objects.all()
            serializer = TicketForVendorSerializer(ticket, many=True)
            return Response(serializer.data)
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        """  
        For change the status of ticket by vendor
        """
        data = request.data
        user = request.user
        if user.type == 'Vendor':
            ticket_status = bool(data['status'])
            ticket_id = data['ticket_id']
            Ticket.objects.filter(
                id=ticket_id).update(is_accepted_by_vendor=ticket_status)
            return Response({"message": "Ticket status updated successfuly by vendor"})
        else:
            content = {"message": "you are not permited to do this action"}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
