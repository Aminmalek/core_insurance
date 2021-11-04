from rest_framework import status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.models import InsuranceConnector
from . models import Ticket, Claim
from . serializers import TicketSerializer, ClaimSerializer
from Core.decorators import type_check


class TicketView(APIView):

    @type_check(["Company","Holder","SuperHolder","Insured"])
    def get(self, request):
        user = request.user
        if user.type == 5 or user.type == 4  or user.type == 3  or user.type == 2:
            tickets = Ticket.objects.filter(user=user)
        elif user.type == 1:
            tickets = Ticket.objects.all()
        else:
             return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    @type_check(["Holder","SuperHolder","Insured"])
    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 5 or user.type == 4  or user.type == 3  or user.type == 2:
            ticket_name = data['name']
            description = data['description']
            Ticket.objects.create(
                user=user, name=ticket_name, status='Opened', description=description)
            return Response({"message": "Ticket created successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    @type_check(["Company"])
    def put(self, request, id):
        data = request.data
        user = request.user
        if user.type == 1:
            ticket = Ticket.objects.get(id=id)
            ticket_status = data['status']
            description = data['description']
            if ticket_status:
                ticket.status = ticket_status
            if description:
                ticket.description = description
            ticket.save()
            return Response({"message": "Ticket updated successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)


class ClaimView(APIView):

    @type_check(["Company","Holder","SuperHolder","Insured"])
    def get(self, request, id=None):
        user = request.user
        print(id)
        if user.type == 4 or user.type == 5 or user.type == 3:
            if id:
                claims = Claim.objects.get(id=id, user=user)
                serializer = ClaimSerializer(claims)
            else:
                claims = Claim.objects.filter(user=user)
                serializer = ClaimSerializer(claims, many=True)

        elif user.type == 1:
            if id:
                claims = Claim.objects.get(id=id)
                serializer = ClaimSerializer(claims)
            else:
                claims = Claim.objects.all()
                serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)

    @type_check(["Holder","Insured"])
    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 5 or user.type == 4:
            title = data['title']
            insurance_id = data['insurance']
            claim_form = data['claim_form']
            description = data['description']
            insurance = InsuranceConnector.objects.get(id=insurance_id)
            Claim.objects.create(
                user=user, title=title, insurance=insurance, status='Opened', claim_form=claim_form, description=description)
            return Response({"message": "Claim created successfuly"}, status=status.HTTP_200_OK)

    @type_check(["Company","Holder","Insured"])
    def put(self, request, id):
        data = request.data
        user = request.user
        if user.type == 1:
            response = data['response']
            claim_status = data['status']
            claim = Claim.objects.get(id=id)
            claim.response = response
            claim.status = claim_status
            claim.save()
            return Response({"message": "Claim updated successfuly"}, status=status.HTTP_200_OK)
        if user.type == 5 or user.type == 4:
            claim = Claim.objects.get(id=id)
            if claim.status == 'Reopened':
                title = data['title']
                claim_form = data['claim_form']
                insurance_id = data['insurance']
                description = data['description']
                if title:
                    claim.title = title
                if insurance_id:
                    insurance = InsuranceConnector.objects.get(id=insurance_id)
                    claim.insurance = insurance
                if claim_form:
                    claim.claim_form = claim_form
                if description:
                    claim.description = description
                claim.status = 'Opened'
                claim.save()
                return Response({"message": "Claim updated successfuly"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "you can't update your claim without company request"}, status=status.HTTP_403_FORBIDDEN)
       
    @type_check(["Holder","Insured"])
    def delete(self, request, id):
        user = request.user
        claim = Claim.objects.get(id=id)
        if claim.user == user:
            claim.is_archived = True
            claim.save()
            return Response({"message": "Claim archived successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you can only delete your claims"}, status=status.HTTP_403_FORBIDDEN)
    