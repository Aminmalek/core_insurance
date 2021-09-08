from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):

    def setUp(self):

        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.get_user_url = reverse("get-user")

        self.no_data = {

            "username": "",
            "password": ""
        }

        self.correct_register_data = {
            'username': 'amin',
            'password': '123456'
        }
        self.existing_username = {
            'username': 'amin',
            'password': 'Password'
        }
        self.incorrect_login_data = {
            'username': 'amin',
            'password': 'WrongPass',
        }

        self.correct_login_data = {
            'username': 'amin',
            'password': '123456',
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
