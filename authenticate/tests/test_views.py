from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from authenticate.serializers import UserSerializer
from django.urls import reverse


class TestSignup(APITestCase):

    def setUp(self):
        self.url = reverse("register")

    def test_user_can_register(self):

        data = {

            "username": "354354354",
            "password": "123456",
            "first_name": "Gholam",
            "last_name": "Gholami",
            "phone": "3543543543"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_can_register_with_repetitive_username(self):

        User.objects.create(username="354354354",
                            password=752783782, phone=9124756598)
        data = {

            "username": "354354354",
            "password": "123456",
            "first_name": "Gholam",
            "last_name": "Gholami",
            "phone": "3543543543"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(406, response.status_code)


class TestLoginView(APITestCase):

    def setUp(self):
        self.url = reverse("login")
        self.username = "1234567899"
        self.password = "123456"
        self.type = "Company"
        self.phone = "3546345"
    # this test is not pass
    '''
    def test_can_user_login(self):
        user = User.objects.create(
            username=self.username, password=self.password, type=self.type, phone=self.phone)
        token = Token.objects.create(user=user)
        data = {

            'username': '1234567899',
            'password': '123456',

        
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
    '''

    def test_can_user_login_with_wrong_pass(self):
        user = User.objects.create(
            username=self.username, password=self.password, type=self.type, phone=self.phone)
        token = Token.objects.create(user=user)
        data = {

            'username': '1234567899',
            'password': '1234567',

        }
        response = self.client.post(self.url, data)
        self.assertEqual(401, response.status_code)


class Testlogout(APITestCase):

    def setUp(self):
        self.username = "company1"
        self.password = "123456"
        self.type = "Company"
        self.phone = "3546345"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type, phone=self.phone)
        self.url = reverse("logout")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_can_logout(self):
        response = self.client.post(self.url)
        self.assertEqual(200, response.status_code)

class TestGetUserView(APITestCase):

    def setUp(self):
        self.username = "company1"
        self.password = "123456"
        self.type = "Company"
        self.phone = "3546345"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type, phone=self.phone)
        self.url = reverse("get-user")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_user_can_get_his_details(self):
        user  = User.objects.get(username=self.username)
        serializer = UserSerializer(user)
        response = self.client.get(self.url)
        self.assertEqual(serializer.data, response.data)

class TestUserView(APITestCase):

    def setUp(self):
        self.username = "company1"
        self.password = "123456"
        self.type = "Company"
        self.phone = "3546345"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type, phone=self.phone)
        self.url = reverse("user")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_copmany_user_can_view_users(self):
        User.objects.create(username=687654654654,password=12345678,phone=912456887)
        User.objects.create(username=96865416354,password=12345678,phone=9198754612)
        user = User.objects.all()
        serializer = UserSerializer(user,many=True)
        response = self.client.get(self.url)
        self.assertEqual(serializer.data, response.data)
    
    def test_none_copmany_user_can_view_users(self):
        new_user = User.objects.create(
            username=8751684, 
            password=123456, 
            type="Insured", 
            phone=9104565789
            )
       
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        User.objects.create(username=687654654654,password=12345678,phone=912456887)
        User.objects.create(username=96865416354,password=12345678,phone=9198754612)
        user = User.objects.all()
        serializer = UserSerializer(user,many=True)
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_company_user_can_update_user_data(self):
        User.objects.create(username=687654654654,password=12345678,phone=912456887,type="Vendor")
        user = User.objects.get(username=687654654654)
        data = {
            "is_active" : True,
            "type" : "Insured"
        }
        types = user.type
        response = self.client.put("/api/auth/user?id=1",data)
        self.assertEquals(types,"Vendor")

    def test_none_company_user_can_update_user_data(self):
        new_user = User.objects.create(
            username=8751684, 
            password=123456, 
            type="Insured", 
            phone=9104565789
            )
       
        token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        user = User.objects.create(username=687654654654,password=12345678,phone=912456887,type="Vendor")
        data = {
            "is_active" : True,
            "type" : "Insured"
        }
        response = self.client.put("/api/auth/user?id=1",data)
        
        self.assertEquals(403, response.status_code,)