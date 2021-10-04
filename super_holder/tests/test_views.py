from insured.models import Insured
from insurance.models import Insurance
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from django.urls import reverse


class SuperHolderTests(APITestCase):

    def setUp(self):

        self.username = "insured1"
        self.password = "123456"
        self.type = "SuperHolder"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)
        self.insured = Insured.objects.create(user=self.user)
        self.url = reverse("superholder")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_Company_view_superHolders(self):
        company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Company")
        new_token = Token.objects.create(user=company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
    
    def test_user_superHolder_can_view_or_create_superHolders(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
    
    def test_user_none_superHolder_or_company_can_view_or_create_superHolders(self):
        some_user = User.objects.create(
            username="company", password="123456", type="Vendor")
        new_token = Token.objects.create(user=some_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)
    
    '''
    def test_none_company_user_can_delete_insureds(self):
        company_user = User.objects.create(
            username="company", password="123456", type="Vendor")
        new_token = Token.objects.create(user=company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        Insured.objects.create(user=user)
        data = {"user_id":user.id}
        response = self.client.delete(self.url,data)
        self.assertEqual({"message": "you are not authorized to perform this action"}, response.data)
    '''