from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from payment.models import InsuranceConnector
from ticket.models import Claim, Ticket
from django.urls import reverse
from ticket.serializers import TicketSerializer
from insurance.models import Insurance


'''
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
        self.assertEqual(200, response.status_code)

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
        self.assertEqual(200, response.status_code)

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
        self.assertEqual(403, response.status_code)

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
'''
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

class ClaimTests(APITestCase):

    def setUp(self):
        """ Tests setup and register user
        """
        self.username = "user1"
        self.password = "123456"
        self.type = "Insured"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)
        self.url = reverse("claim")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_Insured_can_view_his_claims(self):
        
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_user_Holder_can_view_his_claims(self):
        insured_user = User.objects.create(
            username="35685754", password="123456", type="Holder")
        self.new_token = Token.objects.create(user=insured_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_user_Company_can_view_all_claims(self):
        insured_user = User.objects.create(
            username="35685754", password="123456", type="Company")
        self.new_token = Token.objects.create(user=insured_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_user_Insured_can_post_claims(self):
        InsuranceConnector.objects.create(user=self.user,)
        data = {"title": "some insurance!",
                "insurance": 1,
                "description": "this is an insurance",
                "claim_form": {"where": "Tehran",
                                "wich city": "Tehran",
                                "how much": 8456,
                                "when": "1400/02/05"}
                }

        response = self.client.post(self.url,format='json',data=data)
        self.assertEqual({"message": "Claim created successfuly"}, response.data)

    def test_user_Holder_can_post_claims(self):
        holder_user = User.objects.create(
            username="35685754", password="123456", type="Holder")
        self.new_token = Token.objects.create(user=holder_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        InsuranceConnector.objects.create(id=2,user=self.user,)
        data = {"title": "some insurance!",
                "insurance": 2,
                "description": "this is an insurance",
                "claim_form": {"where": "Tehran",
                                "wich city": "Tehran",
                                "how much": 8456,
                                "when": "1400/02/05"}
                }

        response = self.client.post(self.url,format='json',data=data)
        self.assertEqual({"message": "Claim created successfuly"}, response.data)

    def test_some_user_can_post_claims(self):
        holder_user = User.objects.create(
            username="35685754", password="123456", type="Vendor")
        self.new_token = Token.objects.create(user=holder_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        InsuranceConnector.objects.create(id=2,user=self.user,)
        data = {"title": "some insurance!",
                "insurance": 2,
                "description": "this is an insurance",
                "claim_form": {"where": "Tehran",
                                "wich city": "Tehran",
                                "how much": 8456,
                                "when": "1400/02/05"}
                }

        response = self.client.post(self.url,format='json',data=data)
        self.assertEqual({"message": "you are not authorized to perform this action"}, response.data)

    def test_Company_can_change_claim_status(self):
        _user = User.objects.create(
        username="35685754", password="123456", type="Company")
        self.new_token = Token.objects.create(user=_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        InsuranceConnector.objects.create(id=2,user=self.user,)
        con = InsuranceConnector.objects.get(id=2)
        Claim.objects.create(id=745,title="some insurance!",
        insurance=con,
        description="this is an claim",
        claim_form={"where": "Tehran",
                                "wich city": "Tehran",
                                "how much": 8456,
                                "when": "1400/02/05"})
        data_put = {
                "response":"this must be paid!!",
                "status": "Approved",     
        }
        
        response = self.client.put("/api/claim/745",format='json',data=data_put)
        self.assertEqual({"message": "Claim updated successfuly"}, response.data)