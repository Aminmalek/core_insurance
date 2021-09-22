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
        self.type = "Insured"
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
            username="mamad_gholi", password="123456", type="Company")
        new_token = Token.objects.create(user=company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_none_company_canview_all_insureds(self):
        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Vendor")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_holder_can_post_user(self):
        user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        data = {"user_id":user.id}
        response = self.client.post(self.url,data)
        self.assertEqual(201, response.status_code)

    def test_company_user_can_delete_insureds(self):
        company_user = User.objects.create(
            username="company", password="123456", type="Company")
        new_token = Token.objects.create(user=company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        Insured.objects.create(user=user)
        data = {"user_id":user.id}
        response = self.client.delete(self.url,data)
        self.assertEqual(200, response.status_code)

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
    def test_user_none_copmany_can_post_insurances(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        data = {"name": "some insurance!",
                "description": "this is an insurance but i'm not companyyy!"}
        response = self.client.post(self.url, data)
        self.assertEqual(401, response.status_code)

    def test_user_copmany_can_post_duplicate_insurances(self):

        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")
        data = {"name": "some insurance!",
                "description": "this is an insurance"}
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_copmany_can_update_insurances(self):

        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")
        data = {"id": 1, "name": "some thing",
                "description": "this is an updated insurance !"}
        response = self.client.put(self.url, data)
        self.assertEqual(202, response.status_code)

    def test_user_none_copmany_can_update_insurances(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")
        data = {"id": 1, "name": "some thing",
                "description": "this is an updated insurance !"}
        response = self.client.put(self.url, data)
        self.assertEqual(401, response.status_code)

    def test_user_copmany_can_delete_insurances(self):

        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")
        data = {"id": 1}
        response = self.client.delete(self.url, data)
        self.assertEqual(202, response.status_code)

    def test_user_none_copmany_can_delete_insurances(self):
        
        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")
        data = {"id": 1}
        response = self.client.delete(self.url, data)
        self.assertEqual(401, response.status_code)
        '''
