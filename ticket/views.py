import re
import json
import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authenticate.models import User
from payment.models import InsuranceConnector
from . models import Ticket, Claim
from . serializers import TicketSerializer, ClaimSerializer
from Core.decorators import type_check
from Health_Insurance.settings import BASE_DIR
from .models import ReviewerTimeline
from insurance.models import Coverage


class TicketView(APIView):

    @type_check(["Company", "Holder", "SuperHolder", "Insured", ])
    def get(self, request):
        user = request.user
        if user.type == 5 or user.type == 4 or user.type == 3 or user.type == 2:
            tickets = Ticket.objects.filter(user=user)
        elif user.type == 1:
            tickets = Ticket.objects.all()
        else:
            return Response({"message": "you are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    @type_check(["Company", "Holder", "SuperHolder", "Insured", "Vendor"])
    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 5 or user.type == 4 or user.type == 3 or user.type == 2:
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
    
    def claim_form_uuid_generator(self, object):
        
        for item in object:
            if 'id' not in item:
                item['id'] = str(uuid.uuid4())
        return object

    @type_check(["Company", "Holder", "SuperHolder", "Insured", 'CompanyAdmin'])
    def get(self, request, id=None):
        user = request.user
        if user.type == 4 or user.type == 5 or user.type == 3:
            if id:
                claims = Claim.objects.get(id=id, user=user)
                serializer = ClaimSerializer(claims)
            else:
                claims = Claim.objects.filter(user=user)
                serializer = ClaimSerializer(claims, many=True)

        elif user.type == 1 or user.type == 6:
            if id:
                claims = Claim.objects.get(id=id)
                serializer = ClaimSerializer(claims)
            else:
                claims = Claim.objects.all()
                serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)

    @type_check(["Holder", "Insured", "Company", "SuperHolder", "CompanyAdmin"])
    def post(self, request):
        data = request.data
        user = request.user
        if user.type == 5 or user.type == 4 or user.type == 3:
            title = data['title']
            insurance = data['insurance_id']
            claims_form = data['claim_form']
            description = data['description']
            claimed_amount = data['claimed_amount']
            claim_date = data['claim_date']
            coverage = data['coverage']
            insurance = InsuranceConnector.objects.get(id=insurance)
            claim = Claim.objects.create(
                user=user, title=title, insurance=insurance, status='Opened', claim_form=claims_form, description=description,
                claimed_amount=claimed_amount, claim_date=claim_date)
            for objects in coverage:
                claim_form=self.claim_form_uuid_generator(objects["claim_form"])
                cover = Coverage.objects.create(
                    name=objects['name'], claim_form=claim_form, capacity=objects['capacity'])
                claim.coverage.add(cover)
            return Response({"message": "Claim created successfuly"}, status=status.HTTP_200_OK)

        elif user.type == 1 or user.type == 6:
            username = data['username']
            insurance = data['insurance_id']
            description = data['description']
            claims_form = data['claim_form']
            coverage = data['coverage']
            claimed_amount = data['claimed_amount']
            claim_date = data['claim_date']
            user = User.objects.get(username=username)
            insurance = InsuranceConnector.objects.get(id=insurance)
            claim = Claim.objects.create(
                user=user, insurance=insurance, status='Opened', claim_form=claims_form,
                description=description, claimed_amount=claimed_amount, claim_date=claim_date)
            for objects in coverage:
                claim_form=self.claim_form_uuid_generator(objects["claim_form"])
                cover = Coverage.objects.create(
                    name=objects['name'], claim_form=claim_form, capacity=objects['capacity'])
                claim.coverage.add(cover)

            return Response({"message": "Claim created successfuly"}, status=status.HTTP_200_OK)

    @type_check(["Company", "Holder", "Insured", "SuperHolder", 'CompanyAdmin'])
    def put(self, request, id):
        data = request.data
        user = request.user
        if user.type == 1 or user.type == 6:
            response = data['response']
            claim_status = data['status']
            reviewer = data['reviewer']
            insurance = data['insurance']
            franchise = data['franchise']
            tariff = data['tariff']
            payable_amount = data['payable_amount']
            deductions = data['deductions']
            vendor = data['vendor']
            specefic_name = data['specefic_name']
            coverage = data['coverage']
            insurance = InsuranceConnector.objects.get(id=insurance)
            claim = Claim.objects.get(id=id)
            if reviewer:
                reviewer_user = User.objects.get(username=reviewer)
                timeline = ReviewerTimeline.objects.create(
                    changed_by=user, reviewer=reviewer_user)
                claim.reviewer = reviewer_user
                claim.reviewer_timeline.add(timeline)
            if vendor:
                vendor = User.objects.get(username=vendor)
                claim.vendor = vendor
            if response:
                claim.response = response
            if claim_status:
                claim.status = claim_status
            if insurance:
                claim.insurance = insurance
            if franchise:
                claim.franchise = franchise
            if tariff:
                claim.tariff = tariff
            if payable_amount:
                claim.payable_amount = payable_amount
            if deductions:
                claim.deductions = deductions
            if specefic_name:
                claim.specefic_name = specefic_name
            if coverage:
                claim.coverage.clear()
                for objects in coverage:
                    claim_form=self.claim_form_uuid_generator(objects["claim_form"])
                    cover = Coverage.objects.create(
                        name=objects['name'],claim_form=claim_form , capacity=objects['capacity'])
                    claim.coverage.add(cover)
            claim.save()
            return Response({"message": "Claim updated successfuly"}, status=status.HTTP_200_OK)

        if user.type == 5 or user.type == 4 or user.type == 3:
            
            claim = Claim.objects.get(id=id)
            if user != claim.user:
                return Response({"error": "user only can update his claims"}, status=status.HTTP_403_FORBIDDEN)
                
            if claim.status == 'Opened':
                title = data['title']
                claims_form = data['claim_form']
                insurance_id = data['insurance']
                description = data['description']
                coverage = data['coverage']
                claimed_amount = data['claimed_amount']
                claim_date = data['claim_date']
                if title:
                    claim.title = title
                if insurance_id:
                    insurance = InsuranceConnector.objects.get(id=insurance_id)
                    claim.insurance = insurance
                if claims_form:
                    claim.claim_form = claims_form
                if description:
                    claim.description = description
                if coverage:
                    claim.coverage.clear()
                    for objects in coverage:
                        claim_form=self.claim_form_uuid_generator(objects["claim_form"])
                        cover = Coverage.objects.create(
                            name=objects['name'],claim_form=claim_form , capacity=objects['capacity'])
                        claim.coverage.add(cover)
                if claimed_amount:
                    claim.claimed_amount = claimed_amount
                if claim_date:
                    claim.claim_date = claim_date
                claim.save()
                return Response({"message": "Claim updated successfuly"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "user can't update your claim without company request"}, status=status.HTTP_403_FORBIDDEN)

    @type_check(["Holder", "Insured", "SuperHolder"])
    def delete(self, request, id):
        user = request.user
        claim = Claim.objects.get(id=id)
        if claim.user == user:
            claim.is_archived = True
            claim.save()
            return Response({"message": "Claim archived successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "you can only delete your claims"}, status=status.HTTP_403_FORBIDDEN)


class DataVendorView(APIView):
    """
        For search in a medical json file
    """
    @type_check(["Vendor", "Company"])
    def get(self, request):
        searched_name = request.query_params.get('name', None)
        with open(BASE_DIR / 'data' / 'data.json', encoding='utf-8-sig') as file:
            data = json.load(file)
            user_needed_rows = []
            for row in data:
                regx = re.search(str(searched_name), str(row))
                if regx:
                    user_needed_rows.append(row)
        return Response(user_needed_rows)
