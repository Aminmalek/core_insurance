'''
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from ticket.models import Ticket
from django.urls import reverse


class NotCopmanyTests(APITestCase):

    def setUp(self):

        self.username = "company1"
        self.password = "123456"
        self.type = "Company"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)
        self.url = reverse("ticket-company")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_notcopmany_view_tickets(self):

        none_company_user = User.objects.create(
            username="hasan_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_company_user_can_view_tickets(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_company_can_put_tickets(self):

        ticket = Ticket.objects.create(
            name="bime takmili", description="hello!")
        data = {"status": "True", "ticket_id": 1}
        response = self.client.put(self.url, data)
        self.assertEqual(
            {'message': 'Ticket status updated successfuly by company'}, response.data)

    def test_none_company_can_put_tickets(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        ticket = Ticket.objects.create(
            name="bime takmili", description="hello!")
        data = {"status": "True", "ticket_id": 1}
        response = self.client.put(self.url, data)
        self.assertEqual(401, response.status_code)


class VendoreActivationTests(APITestCase):

    def setUp(self):

        self.username = "company1"
        self.password = "123456"
        self.type = "Company"
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type)
        self.url = reverse("vendor-avtivation")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_post_vendor_by_company(self):
        """ Test that Company user can post username of vendor and see the activation status"""
        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Vendor", is_active=False)
        data = {"vendor_username": "mamad_gholi"}
        response = self.client.post(self.url, data)
        self.assertEqual({'user activated': False}, response.data)

    def test_post_vendor_by_none_company(self):
        """ Test that Company user can post username of vendor and see the activation status
        """
        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Insured")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        vendor_user = User.objects.create(
            username="mamad_hasan", password="123456", type="Vendor", is_active=False)
        data = {"vendor_username": "mamad_gholi"}
        response = self.client.post(self.url, data)
        self.assertEqual(401, response.status_code)

    def test_active_vendor_by_company(self):
        """ Test Company user can active or deactive the user by send username and new status
        """ 
        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Vendor", is_active=False)
        data = {"vendor_username": "mamad_gholi",
                "vendor_activation_status": True}
        response = self.client.put(self.url, data)
        self.assertEqual(
            {"message": "vendor activation status changed successfuly"}, response.data)
        
    
    def test_active_vendor_by_none_company(self):
        """ Test none-Company user can active or deactive the user by send username and new status
        """
        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type="Vendor")
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        vendor_user = User.objects.create(
            username="mamad_hasan", password="123456", type="Vendor", is_active=False)
        data = {"vendor_username": "mamad_hasan",
                "vendor_activation_status": True}
        response = self.client.put(self.url, data)
        self.assertEqual(401, response.status_code)

    def test_active_vendor_by_company_with_incorrect_data(self):
            """ Test Company user can active or deactive the user by send username and new status
            """ 
            company_user = User.objects.create(
                username="mamad_gholi", password="123456", type="Vendor", is_active=False)
            data = {"vendor_username": "mamad",
                    "vendor_activation_status": True}
            response = self.client.put(self.url, data)
            self.assertEqual(404, response.status_code)
'''