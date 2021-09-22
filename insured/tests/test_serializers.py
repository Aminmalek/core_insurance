from rest_framework import serializers
from ticket.models import Ticket
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from company.serializers import TicketForCompanySerializer
from authenticate.models import User

'''
class TestSerliazers(APITestCase):

    def test_serializer(self):
        ser_data = {
                "name": "bime1",
                "username": "mamad_gholi",
                "description": "this is an insurance",
                "is_accepted_by_vendor": False,
                "is_accepted_by_company": False,
                "has_withdrawed": False
            } 
        user = User.objects.create(
            username="mamad_gholi", password="123456", type="Vendor")
        self.ticket = Ticket.objects.create(
            name="bime1", description="this is an insurance", user=user)
        self.serializer = TicketForCompanySerializer(self.ticket)

        self.assertEqual(ser_data,self.serializer.data)
'''