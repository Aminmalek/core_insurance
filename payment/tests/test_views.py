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
        self.username = "35465635241"
        self.password = "123456"
        self.type = 4
        self.cash = 500
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type,cash=self.cash)
        self.url = reverse("insurance_connector")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    
    def test_1_user_vendor_cant_view_insurance_connectors(self):
        user = User.objects.create(
            username="company", password="123456", type=2)
        Ticket.objects.create(name="some ticket",
                              user=user, description="some thing")
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_2_user_can_view_insurance_connectors(self):
        user = User.objects.create(
            username="company", password="123456", type=1)
        Ticket.objects.create(name="some ticket",
                              user=user, description="some thing")
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_3_holder_can_post_insurance_connector(self):
        Insurance.objects.create(id=847,name="insu", description="some thing",price=25)
        data = {
            "insurance_id": 847,
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

    def test_4_users_cash_reduced_after_buying_insurance(self):
        Insurance.objects.create(id=87,name="insu", description="some thing",price=25)
        data = {
            "insurance_id": 87,
            "register_form": {"single": "yes",
                              "sallery": 684,
                              "childes": "No",
                              "sickness": "NO",
                              "sickness name": "NO"
                              }
        }
        
        response = self.client.post(self.url, format='json', data=data)
        user = User.objects.get(username=self.username)
        connector = InsuranceConnector.objects.get(insurance=87)
        self.assertEqual(500-25,user.cash)

    def test_5_users_type_changes_after_buy_insurance(self):
        user = User.objects.create(
            username="54875466", password="123456", type=5,cash=878)
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        Insurance.objects.create(id=54,name="insu", description="some thing",price=25)
        data = {
            "insurance_id": 54,
            "register_form": {"single": "yes",
                              "sallery": 684,
                              "childes": "No",
                              "sickness": "NO",
                              "sickness name": "NO"
                              }
        }
        
        response = self.client.post(self.url, format='json', data=data)
        user = User.objects.get(username="54875466")
        connector = InsuranceConnector.objects.get(insurance=54)
        self.assertEqual(4,user.type)

    def test_6_error_if_user_money_is_low(self):
        user = User.objects.create(
            username="54875466", password="123456", type=5,cash=8)
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        Insurance.objects.create(id=54,name="insu", description="some thing",price=25)
        data = {
            "insurance_id": 54,
            "register_form": {"single": "yes",
                            "sallery": 684,
                            "childes": "No",
                            "sickness": "NO",
                            "sickness name": "NO"
                            }
        }
        
        response = self.client.post(self.url, format='json', data=data)  
        self.assertEqual(400,response.status_code)
        self.assertEqual({"error":"you have not enough money to buy insurance"},response.data)

    def test_7_is_paid_changes_after_buy_insurance(self):
        user = User.objects.create(
            username="54875466", password="123456", type=5,cash=878)
        self.new_token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.new_token.key)
        Insurance.objects.create(id=54,name="insu", description="some thing",price=25)
        data = {
            "insurance_id": 54,
            "register_form": {"single": "yes",
                                "sallery": 684,
                                "childes": "No",
                                "sickness": "NO",
                                "sickness name": "NO"
                                }
        }
        
        response = self.client.post(self.url, format='json', data=data)
        user = User.objects.get(username="54875466")
        connector = InsuranceConnector.objects.get(insurance=54)
        self.assertEqual(True,connector.is_paid)

    def test_8_company_can_update_insurance_connector(self):
        user=User.objects.create(
            username = "42742452452", password = "123456", type = 1)
        self.new_token=Token.objects.create(user = user)
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token ' + self.new_token.key)
        insurance=Insurance.objects.create(
            id=874,name = "insu", description = "some thing")
        InsuranceConnector.objects.create(id = 874, user = self.user,
                                          insurance = insurance,
                                          register_form = {"single": "yes",
                                                         "sallery": 684,
                                                         "childes": "No",
                                                         "sickness": "yes",
                                                         "sickness name": "AIDS"
                                                         },
                                                         is_accepted_by_company=False)
        data={
            "is_accepted_by_company": "true",
        }
        response = self.client.put(
            "/api/insurance_connector/874", format = 'json', data = data)
        connector = InsuranceConnector.objects.get(insurance=874)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, connector.is_accepted_by_company)

    def test_9_none_holder_user_can_post_insurance_connector(self):
        user = User.objects.create(
            username="company", password="123456", type=1)
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

    def test_10_some_user_can_update_insurance_connector(self):
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

   