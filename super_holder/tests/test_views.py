from insurance.models import Insurance
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from insured.models import Insured
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
        self.assertEqual(403, response.status_code)

    def test_superholder_can_add_holder(self):
        user = User.objects.create(
            username="super1", password="123456", type="SuperHolder")
        super_holder = SuperHolder.objects.create(user=user)
        new_token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        user2 = User.objects.create(id=125,username='2121215485', password='123456',type="Holder")
        user3 = User.objects.create(id=498,username='8765465468', password='123456',type="Holder")
        data1 = {"supported_holders": user2.id}
        data2 = {"supported_holders": user3.id}
        response = self.client.put('/api/superholder', data1)
        response = self.client.put('/api/superholder', data2)
        super_holder = SuperHolder.objects.get(user=user)
        supported = super_holder.supported_holders.all()
        ids_list = []
        ids_must_be = [125,498]
        for user in supported:
            id = user.id
            ids_list.append(id)
        
        self.assertEqual(ids_list, ids_must_be)
        self.assertEqual(200, response.status_code)
        
    def test_superholder_can_delete_holder(self):
        holder1 = User.objects.create(id=564,username='001245789', password='123456',type="Holder")
        holder2 = User.objects.create(id=548,username='021654654', password='123456',type="Holder")
        Insured.objects.create(user=holder1)
        Insured.objects.create(user=holder2)
        super_holder = SuperHolder.objects.create(user=self.user)
        user1 = User.objects.get(id=564)
        user2 = User.objects.get(id=548)
        super_holder.supported_holders.add(user1)
        super_holder.supported_holders.add(user2)

        response = self.client.delete('/api/superholder/564')
        self.assertEqual({"message": "Holder deleted successfuly"},response.data)
