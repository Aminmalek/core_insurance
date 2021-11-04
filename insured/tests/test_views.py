from insured.models import Insured
from insurance.models import Insurance
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from django.urls import reverse


class InsuredTests(APITestCase):

    def setUp(self):

        self.username = "insured1"
        self.password = "123456"
        self.type = 5
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)
        self.insured = Insured.objects.create(user=self.user)
        self.url = reverse("insured")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_insured_view_datas(self):

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_company_canview_all_insureds(self):
        company_user = User.objects.create(
            username="mamad_gholi", password="123456", type=1)
        new_token = Token.objects.create(user=company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_none_company_canview_all_insureds(self):
        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type=2)
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_holder_can_post_user(self):
        holder = User.objects.create(
            username="54654", password="123456", type=4)
        new_token = Token.objects.create(user=holder)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        user = User.objects.create(
            username="mamad_gholi", password="123456", type=5)
        Insured.objects.create(user=holder)
        data = {
                "username": 6546876584,
                "password": "25448576857",
                "first_name": "amin",
                "last_name": "malek",
                "phone": "9124578945",
                "bank_account_number":87687646587687687685
                }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_company_user_can_delete_insureds(self):
        company_user = User.objects.create(
            username="5465765", password="123456", type=1)
        new_token = Token.objects.create(user=company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        user = User.objects.create(
            username="mamad_gholi", password="123456", type=5)
        Insured.objects.create(user=user)
        response = self.client.delete('/api/insured/'+str(user.id))
        self.assertEqual(200, response.status_code)

    def test_none_company_user_can_delete_insureds(self):
        company_user = User.objects.create(
            username="5457657", password="123456", type=2)
        new_token = Token.objects.create(user=company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        user = User.objects.create(
            username="mamad_gholi", password="123456", type=5)
        Insured.objects.create(user=user)
        response = self.client.delete('/api/insured/'+str(user.id))
        self.assertEqual(
            {"message": "you are not authorized to perform this action"}, response.data)
