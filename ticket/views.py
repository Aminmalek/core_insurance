from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . models import Ticket
from .models import Ticket
from . serializers import TicketSerializer


class TicketView(APIView):
    def get(self, request):
        user = request.user
        if user.type == 'Holder' or user.type == 'Insured':
            tickets = Ticket.objects.filter(user=user)
        elif user.type == 'Company':
            tickets = Ticket.objects.all()

        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 'Insured' or user.type == 'Holder':
            ticket_name = data['name']
            description = data['description']
            Ticket.objects.create(
                user=user, name=ticket_name, description=description)
            return Response({"message": "Ticket created successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        data = request.data
        user = request.user
        if user.type == 'Company':
            is_accepted_by_company = data['is_accepted_by_company']
            ticket = Ticket.objects.get(id=id)
            if is_accepted_by_company:
                ticket.is_accepted_by_company = True if is_accepted_by_company == 'true' else False
            ticket.save()
            return Response({"message": "Ticket updated successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
