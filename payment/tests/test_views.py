from payment.models import InsuranceConnector
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from ticket.models import Ticket
from django.urls import reverse
from insurance.models import Insurance


class PaymentTests(APITestCase):

    def setUp(self):
        """ Tests setup and register user
        """
        self.username = "Vendor1"
        self.password = "123456"
        self.type = "Holder"
        self.cash = 500
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type,cash=self.cash)
        self.url = reverse("insurance_connector")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_5_holder_can_update_insurance_connector(self):
        insurance=Insurance.objects.create(
            name = "insu", description = "some thing",price=110)
        InsuranceConnector.objects.create(id = 874, user = self.user,
                                          insurance = insurance,
                                          register_form = {"single": "yes",
                                                         "sallery": 684,
                                                         "childes": "No",
                                                         "sickness": "yes",
                                                         "sickness name": "AIDS"
                                                         })
        data={
            "insurance_id": insurance.id,
            "is_accepted_by_company": True,
            "is_paid": True,
            "payment_code": 35465,
            "register_form": {"single": "yes",
                              "sallery": 684,
                              "childes": "No",
                              "sickness": "NO",
                              "sickness name": "NO"
                              }
        }

        response = self.client.put(
            "/api/insurance_connector/874", format = 'json', data = data)
        self.assertEqual(200, response.status_code)
        user = User.objects.get(username=self.username)
        self.assertEqual(390,user.cash)
        
'''
    def test_1_user_vendor_cant_view_insurance_connectors(self):
        user = User.objects.create(
            username="company", password="123456", type="Vendor")
        Ticket.objects.create(name="some ticket",
                              user=user, description="some thing")
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_2_user_can_view_insurance_connectors(self):
        user = User.objects.create(
            username="company", password="123456", type="Company")
        Ticket.objects.create(name="some ticket",
                              user=user, description="some thing")
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_3_holder_can_post_insurance_connector(self):
        Insurance.objects.create(id=87,name="insu", description="some thing")
        data = {
            "insurance_id": 87,
            "is_accepted_by_company": True,
            "is_paid": True,
            "payment_code": 35465,
            "register_form": {"single": "yes",
                              "sallery": 684,
                              "childes": "No",
                              "sickness": "NO",
                              "sickness name": "NO"
                              }
        }
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(201, response.status_code)

    def test_4_none_holder_user_can_post_insurance_connector(self):
        user = User.objects.create(
            username="company", password="123456", type="Company")
        Ticket.objects.create(name="some ticket",
                              user=user, description="some thing")
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        Insurance.objects.create(id=125, name="insu", description="some thing")
        data = {
            "insurance_id": 125,
            "is_accepted_by_company": True,
            "is_paid": True,
            "payment_code": 35465,
            "register_form": {"single": "yes",
                              "sallery": 684,
                              "childes": "No",
                              "sickness": "NO",
                              "sickness name": "NO"
                              }
        }
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(403, response.status_code)


    def test_6_some_user_can_update_insurance_connector(self):
        user=User.objects.create(
            username = "company", password = "123456",)
        Ticket.objects.create(name = "some ticket",
                              user = user, description = "some thing")
        self.new_token=Token.objects.create(user = user)
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token ' + self.new_token.key)
        insurance=Insurance.objects.create(
            name = "insu", description = "some thing")
        InsuranceConnector.objects.create(id = 874, user = self.user,
                                          insurance = insurance,
                                          register_form = {"single": "yes",
                                                         "sallery": 684,
                                                         "childes": "No",
                                                         "sickness": "yes",
                                                         "sickness name": "AIDS"
                                                         })
        data={
            "is_accepted_by_company": True,
            "register_form": {"single": "yes",
                              "sallery": 684,
                              "childes": "No",
                              "sickness": "NO",
                              "sickness name": "NO"
                              },

        }
        response = self.client.put(
            "/api/insurance_connector/874", format = 'json', data = data)
    def test_7_company_can_update_insurance_connector(self):
        user=User.objects.create(
            username = "company", password = "123456", type = "Company")
        Ticket.objects.create(name = "some ticket",
                              user = user, description = "some thing")
        self.new_token=Token.objects.create(user = user)
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token ' + self.new_token.key)
        insurance=Insurance.objects.create(
            name = "insu", description = "some thing")
        InsuranceConnector.objects.create(id = 874, user = self.user,
                                          insurance = insurance,
                                          register_form = {"single": "yes",
                                                         "sallery": 684,
                                                         "childes": "No",
                                                         "sickness": "yes",
                                                         "sickness name": "AIDS"
                                                         })
        data={
            "is_accepted_by_company": True,
            "register_form": {"single": "yes",
                              "sallery": 684,
                              "childes": "No",
                              "sickness": "NO",
                              "sickness name": "NO"
                              },

        }
        response = self.client.put(
            "/api/insurance_connector/874", format = 'json', data = data)
        self.assertEqual(200, response.status_code)
    '''