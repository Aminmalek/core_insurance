from insurance.models import Insurance
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from super_holder.models import SuperHolder
from django.urls import reverse


class SuperHolderTests(APITestCase):

    def setUp(self):

        self.username = "superholder1"
        self.password = "123456"
        self.type = "SuperHolder"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)

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

    def test_superHolder_can_can_add_holder(self):
        super_holder = SuperHolder.objects.create(user=self.user)
        data = {

            'username': '00125487',
            'password': '123456',
            'first_name': 'amin',
            'last_name': 'malek',
            'bank_account_number': 58596532145645884,
            'phone': 9124578456
        }
        response = self.client.post(self.url, data)
        #supports = super_holder.supported_holders
        self.assertEqual(
            {"message": "holder created successfuly"}, response.data)

    def test_superHolder_can_can_add_holder(self):
        super_holder = SuperHolder.objects.create(user=self.user)
        data = {

            'username': '00125487',
            'password': '123456',
            'first_name': 'amin',
            'last_name': 'malek',
            'bank_account_number': 58596532145645884,
            'phone': 9124578456
        }
        response = self.client.post(self.url, data)
        #supports = super_holder.supported_holders
        self.assertEqual(
            {"message": "holder created successfuly"}, response.data)

    def test_superHolder_can_can_add_repetetive_holder(self):
        super_holder = SuperHolder.objects.create(user=self.user)
        user = User.objects.create(
            username='87542132', password='123456', type='Insured')
        data = {

            'username': '87542132',
            'password': '123456',
            'first_name': 'amin',
            'last_name': 'malek',
            'bank_account_number': 58596532145645884,
            'phone': 9124578456
        }
        response = self.client.post(self.url, data)
        #supports = super_holder.supported_holders
        self.assertEqual(
            {'error': 'Username or Phone number already exists'}, response.data)

    def test_any_user_can_add_holder(self):
        company_user = User.objects.create(
            username="company", password="123456", type="Vendor")
        new_token = Token.objects.create(user=company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        super_holder = SuperHolder.objects.create(user=self.user)
        user = User.objects.create(
            username='87542132', password='123456', type='Insured')
        data = {

            'username': '87542132',
            'password': '123456',
            'first_name': 'amin',
            'last_name': 'malek',
            'bank_account_number': 58596532145645884,
            'phone': 9124578456
        }
        response = self.client.post(self.url, data)
        #supports = super_holder.supported_holders
        self.assertEqual(
            403, response.status_code)

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
