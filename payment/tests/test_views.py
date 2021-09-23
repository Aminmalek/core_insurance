from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from ticket.models import Ticket
from django.urls import reverse
from insurance.models import Insurance


class PaymentTests(APITestCase):

    def setUp(self):
        """ Tests setup and register user
        """
        self.username = "Vendor1"
        self.password = "123456"
        self.type = "Holder"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)
        self.url = reverse("insurance_connector")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_vendor_cant_view_insurance_connectors(self):
        user = User.objects.create(
            username="company", password="123456", type="Vendor")
        Ticket.objects.create(name="some ticket",
                              user=user, description="some thing")
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_user_can_view_insurance_connectors(self):
        user = User.objects.create(
            username="company", password="123456", type="Company")
        Ticket.objects.create(name="some ticket",
                              user=user, description="some thing")
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_holder_can_post_insurance_connector(self):
        Insurance.objects.create(name="insu", description="some thing")
        data = {
            "insurance": 1
        }
        response = self.client.post(self.url,data)
        self.assertEqual(201, response.status_code)
    
    def test_none_holder_user_can_post_insurance_connector(self):
        user = User.objects.create(
            username="company", password="123456", type="Company")
        Ticket.objects.create(name="some ticket",
                              user=user, description="some thing")
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        Insurance.objects.create(name="insu", description="some thing")
        data = {
            "insurance": 1
        }
        response = self.client.post(self.url,data)
        self.assertEqual(401, response.status_code)