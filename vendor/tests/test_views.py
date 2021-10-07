'''
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from ticket.models import Ticket
from django.urls import reverse


class VendorTests(APITestCase):

    def setUp(self):
        """ Tests setup and register vendor user
        """
        self.username = "Vendor1"
        self.password = "123456"
        self.type = "Vendor"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)
        self.url = reverse("ticket-by-vendor")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_vendor_view_tickets(self):

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_none_vendor_can_get_tickets(self):
        fake_user = User.objects.create(
            username="company", password="123456", type="Company")
        new_token = Token.objects.create(user=fake_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_vendor_can_update_ticket(self):
        fake_user = User.objects.create(
        username="company", password="123456", type="Company")
        Ticket.objects.create(name="some ticket", user=fake_user,description="some thing")
        data = {"status":"true","ticket_id":1}
        response = self.client.put(self.url,data)
        self.assertEqual(200,response.status_code)

    def test_none_vendor_can_update_ticket(self):
        fake_user = User.objects.create(
        username="company", password="123456", type="Company")
        Ticket.objects.create(name="some ticket", user=fake_user,description="some thing")
        self.new_token = Token.objects.create(user=fake_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        data = {"status":"true","ticket_id":1}
        response = self.client.put(self.url,data)
        self.assertEqual(401,response.status_code) 
'''