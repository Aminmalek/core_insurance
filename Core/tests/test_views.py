from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from django.urls import reverse
from insurance.models import Insurance
from Core.models import Message


class InsuranceTests(APITestCase):

    def setUp(self):
        self.username = "54872154"
        self.password = "123456"
        self.type = 1
        self.phone = 9128754652
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type, phone=self.phone)
        self.url = reverse("message")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_1_user_copmany_post_messages(self):
        User.objects.create(username=87542165,password=6545454,type=1,phone=94578120)
        data = {"message":"this is my message!","receiver":87542165}
        response = self.client.post(self.url,data)
        self.assertEqual(200, response.status_code)

    def test_2_user_copmany_cant_post_empty_messages(self):
        User.objects.create(username=87542165,password=6545454,type=1,phone=94578120)
        data = {}
        response = self.client.post(self.url,data)
        self.assertEqual(400, response.status_code)

    def test_3_user_can_read_recieved_messages(self):
        User.objects.create(username=87542165,password=6545454,type=1,phone=94578120)
        receiver = User.objects.get(username=87542165)
        Message.objects.create(sender=self.user,message="helloooo this is messageeee!!!",
        receiver=receiver)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_4_user_can_read_his_send_messages(self):
        User.objects.create(username=87542165,password=6545454,type=1,phone=94578120)
        receiver = User.objects.get(username=87542165)
        Message.objects.create(sender=self.user,message="helloooo this is messageeee!!!",
        receiver=receiver)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        

    def test_user_copmany_can_post_insurances(self):
        data = {"name": "some insurance!",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": {"single": "yes",
                                  "sallery": 684,
                                  "childes": "No",
                                  "sickness": "yes",
                                  "sickness name": "AIDS"},

                "claim_form": {"where": "Tehran",
                               "wich city": "Tehran",
                               "how much": 8456,
                               "when": "1400/02/05"}}

        

    def test_user_none_copmany_can_post_insurances(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        data = {"name": "some insurance!",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": {"single": "yes",
                                  "sallery": 684,
                                  "childes": "No",
                                  "sickness": "yes",
                                  "sickness name": "AIDS"},

                "claim_form": {"where": "Tehran",
                               "wich city": "Tehran",
                               "how much": 8456,
                               "when": "1400/02/05"}
                }
        response = self.client.post(self.url,  content_type="multipart/form-data", data=data)
        self.assertEqual(403, response.status_code)

    def test_user_copmany_can_post_duplicate_insurances(self):

        Insurance.objects.create(
            name="some insurance!", description="this is an insurance", price=65465)
        data = {"name": "some insurance!",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": {"single": "yes",
                                  "sallery": 684,
                                  "childes": "No",
                                  "sickness": "yes",
                                  "sickness name": "AIDS"},

                "claim_form": {"where": "Tehran",
                               "wich city": "Tehran",
                               "how much": 8456,
                               "when": "1400/02/05"}
                }
        response = self.client.post(self.url,  format='json', data=data)
        self.assertEqual(400, response.status_code)

    def test_user_copmany_can_update_insurances(self):

        Insurance.objects.create(
            name="bime badane", description="this is an insurance", price=25475, id=875)
        data = {"name": "bime badane",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": {"single": "yes",
                                  "sallery": 684,
                                  "childes": "No",
                                  "sickness": "yes",
                                  "sickness name": "AIDS"},

                "claim_form": {"where": "Tehran",
                               "wich city": "Tehran",
                               "how much": 8456,
                               "when": "1400/02/05"}
                }

        response = self.client.put(
            '/api/insurance/875', format='json', data=data)
        self.assertEqual(202, response.status_code)

    def test_user_none_company_can_update_insurances(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")
        data = {"name": "some insurance!",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": {"single": "yes",
                                  "sallery": 684,
                                  "childes": "No",
                                  "sickness": "yes",
                                  "sickness name": "AIDS"},

                "claim_form": {"where": "Tehran",
                               "wich city": "Tehran",
                               "how much": 8456,
                               "when": "1400/02/05"}
                }
        response = self.client.put(
            '/api/insurance/1', format='json', data=data)
        self.assertEqual(403, response.status_code)

    def test_user_company_can_delete_insurances(self):

        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")
        response = self.client.delete('/api/insurance/1')
        self.assertEqual(202, response.status_code)

    def test_user_none_copmany_can_delete_insurances(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")

        response = self.client.delete('/api/insurance/1')
