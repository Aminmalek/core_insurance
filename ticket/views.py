from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.models import InsuranceConnector
from . models import Ticket, Claim
from . serializers import TicketSerializer, ClaimSerializer


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


class ClaimView(APIView):
    def get(self, request):
        user = request.user
        if user.type == 'Holder' or user.type == 'Insured':
            claims = Claim.objects.filter(user=user)
        elif user.type == 'Company':
            claims = Claim.objects.all()

        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 'Insured' or user.type == 'Holder':
            title = data['title']
            description = data['description']
            insurance_id = data['insurnace']
            insurance = InsuranceConnector.objects.get(id=insurance_id)
            Claim.objects.create(
                user=user, title=title, description=description, insurance=insurance, claim_status='Opened')
            return Response({"message": "Claim created successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        data = request.data
        user = request.user
        if user.type == 'Company':
            response = data['response']
            claim_status = data['status']
            claim = Claim.objects.get(id=id)
            claim.response = response
            claim.status = claim_status
            claim.save()
            return Response({"message": "Claim updated successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
