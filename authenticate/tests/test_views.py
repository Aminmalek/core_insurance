from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client

from .test_setup import TestSetUp


class Test(TestSetUp):

    def test_user_can_register(self):

        response = self.client.post(
            self.register_url, self.correct_register_data)
        response_message = response.data
        self.assertEqual(response.status_code, 201, response_message)

    def test_user_can_register_with_existing_username(self,):

        response = self.client.post(self.register_url, self.existing_username)
        response2 = self.client.post(self.register_url, self.existing_username)
        response_message = response.data
        self.assertEqual(response2.status_code, 406, response_message)

    def test_user_can_login_with_correct_data(self):

        user_register = self.client.post(
            self.register_url, self.correct_register_data,)
        response = self.client.post(self.login_url, self.correct_login_data)
        response_message = response.data
        self.assertEqual(response.status_code, 200, response_message)

    def test_user_can_login_with_wrong_data(self):

        user_register = self.client.post(
            self.register_url, self.correct_register_data,)

        response = self.client.post(self.login_url, self.incorrect_login_data)
        response_message = response.data
        self.assertEqual(response.status_code, 401, response_message)

    def test_user_can_logout_with_correct_data(self):

        user_register = self.client.post(
            self.register_url, self.correct_register_data,)

        # user login
        login = self.client.post(self.login_url, self.correct_login_data)
        token = login.data['token']

        # log out with set header in authorization
        response = self.client.post(
            self.logout_url, HTTP_AUTHORIZATION="Token "+token)

        response_message = response.data

        self.assertEqual(response.status_code, 200, response_message)

    def test_user_can_logout_with_wrong_data(self):

        user_register = self.client.post(
            self.register_url, self.correct_register_data,)

        # user login
        login = self.client.post(self.login_url, self.correct_login_data)
        token = login.data['token']

        # log out with set header in authorization
        response = self.client.post(
            self.logout_url, HTTP_AUTHORIZATION="Token "+token+"grdty")

        response_message = response.data

        self.assertEqual(response.status_code, 401, response_message)

    def test_can_get_userdata_with_correct_data(self):

        user_register = self.client.post(
            self.register_url, self.correct_register_data,)
        login = self.client.post(self.login_url, self.correct_login_data)
        token = login.data["token"]

        # Must set token to header for get user data
        response = self.client.get(
            self.get_user_url, HTTP_AUTHORIZATION=token)
        response_message = response.data

        self.assertEqual(response.status_code, 200, response_message)


    def test_can_get_userdata_with_incorrect_data(self):

        user_register = self.client.post(
            self.register_url, self.correct_register_data,)
        login = self.client.post(self.login_url, self.incorrect_login_data)
        try:
            token = login.data["token"]
            response = self.client.get(
            self.get_user_url, HTTP_AUTHORIZATION=token)
            response_message = response.data
        except:
            response = self.client.get(
            self.get_user_url)
            response_message  = "An empty message!"
        # Must set token to header for get user data
        

        self.assertEqual(response.status_code, 401)
