from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from ticket.models import Ticket
from django.urls import reverse
from ticket.serializers import TicketSerializer


class TicketsTests(APITestCase):

    def setUp(self):
        """ Tests setup and register user
        """
        self.username = "user1"
        self.password = "123456"
        self.type = "Holder"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)
        self.url = reverse("ticket")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_holder_can_add_tickets(self):
        data = {
            "name": "a ticket",
            "description": "some thing!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_insured_can_add_tickets(self):
        insured_user = User.objects.create(
            username="company", password="123456", type="Insured")
        Ticket.objects.create(name="some ticket",
                              user=insured_user, description="some thing")
        self.new_token = Token.objects.create(user=insured_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        data = {
            "name": "a ticket",
            "description": "some thing!",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_holder_can_view_his_tickets(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_user_insured_can_view_his_tickets(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_fake_user_can_view_tickets(self):
        insured_user = User.objects.create(
            username="company", password="123456",)
        Ticket.objects.create(name="some ticket",
                              user=insured_user, description="some thing")
        self.new_token = Token.objects.create(user=insured_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)

        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_ticket_serializers(self):
        insured_user = User.objects.create(
            username="company", password="123456", type="Insured")

        self.new_token = Token.objects.create(user=insured_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        Ticket.objects.create(name="some ticket",
                                       user=insured_user, description="some thing")
        ticket = Ticket.objects.all()
        serializer = TicketSerializer(ticket,many=True)
        response = self.client.get(self.url)
        self.assertEqual(serializer.data, response.data)


'''
    def test_none_vendor_can_update_ticket(self):
        fake_user = User.objects.create(
        username="company", password="123456", type="Company")
        Ticket.objects.create(name="some ticket", user=fake_user,description="some thing")
        self.new_token = Token.objects.create(user=fake_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        data = {"status":"true","ticket_id":1}
        response = self.client.put(self.url,data)
        self.assertEqual(401,response.status_code) '''
