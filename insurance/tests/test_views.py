from insurance.models import Insurance
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from django.urls import reverse


class InsuranceTests(APITestCase):

    def setUp(self):

        self.username = "company1"
        self.password = "123456"
        self.type = 1
        self.phone = 9128754652
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type, phone=self.phone)
        self.url = reverse("insurance")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_1_user_copmany_view_insurances(self):

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_2_user_copmany_can_post_insurances(self):
        data = {"name": "some insurance!",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": [
                    {
                        "type": "rtgh",
                        "title": "test1",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test1"
                    },
                    {
                        "type": "text",
                        "title": "test2",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test2"
                    },
                    {
                        "type": "text",
                        "title": "test3",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test3"
                    }
                ],
                "coverage": [
                    {
                        "name": "عمومی",
                        "claim_form": [
                            {
                                "name": "بیمه",
                                "type": "درمانی"
                            }
                        ],
                        "capacity": 150
                    }
                ]
                }

        response = self.client.post(self.url,  format='json', data=data)
        self.assertEqual(
            {"message": "insurance created successfuly"}, response.data)

    def test_3_user_none_copmany_can_post_insurances(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type=5)
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        data = {"name": "some insurance!",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": [
                    {
                        "type": "frgdfg",
                        "title": "test1",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test1"
                    },
                    {
                        "type": "text",
                        "title": "test2",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test2"
                    },
                    {
                        "type": "text",
                        "title": "test3",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test3"
                    }
                ],

                "coverage": [
                    {
                        "name": "عمومی",
                        "claim_form": [
                            {
                                "name": "بیمه",
                                "type": "درمانی"
                            }
                        ],
                        "capacity": 150
                    }
                ]
                }
        response = self.client.post(self.url,  format='json', data=data)
        
        self.assertEqual(403, response.status_code)

    def test_4_user_copmany_can_post_duplicate_insurances(self):

        Insurance.objects.create(register_form=[],
            name="some insurance!", description="this is an insurance", price=65465)
        data = {"name": "some insurance!",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": [
                    {
                        "type": "ergergerg",
                        "title": "test1",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test1"
                    },
                    {
                        "type": "text",
                        "title": "test2",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test2"
                    },
                    {
                        "type": "text",
                        "title": "test3",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test3"
                    }
                ],

                "coverage": [
                    {
                        "name": "عمومی",
                        "claim_form": [
                            {
                                "name": "بیمه",
                                "type": "درمانی"
                            }
                        ],
                        "capacity": 150
                    }
                ]
                }
        response = self.client.post(self.url,  format='json', data=data)
        self.assertEqual(400, response.status_code)

    def test_5_user_company_can_update_insurances(self):

        insurance = Insurance.objects.create(
            name="bime badane", description="this is an insurance", price=25475, id=5454)
        data = {"name": "bime badane2",
                "description": "this is an insurance",
                "price": "5754",
                "register_form": [
                    {
                        "type": "text",
                        "title": "test1",
                        "options": [
                            {
                                "label": "",
                                "value": ""
                            }
                        ],
                        "required": True,
                        "validation": {
                            "pattern": "",
                            "maxLength": "",
                            "minLength": "",
                            "errorMessage": ""
                        },
                        "placeholder": "test1"
                    },
                ],
                "coverage": [
                    {
                        "name": "عمومی",
                        "claim_form": [
                            {
                                "name": "بیمه",
                                "type": "درمانی"
                            }
                        ],
                        "capacity": 150
                    }
                ]
                }
        
        response = self.client.put(
            '/api/insurance/5454', format='json', data=data)
        self.assertEqual(202, response.status_code)
      
    def test_6_user_none_company_can_update_insurances(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type=5)
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")
        data = {"name": "some insurance!",
                "description": "this is an insurance",
                "price": 5754,
                "register_form": {"single": "yes",
                                  "sallery": 684,
                                  "childes": "No",
                                  "sickness": "yes",
                                  "sickness name": "AIDS"},

                "coverage": [
                    {
                        "name": "عمومی",
                        "claim_form": [
                            {
                                "name": "بیمه",
                                "type": "درمانی"
                            }
                        ],
                        "capacity": 150
                    }
                ]
                }
        response = self.client.put(
            '/api/insurance/1', format='json', data=data)
        self.assertEqual(403, response.status_code)

    def test_7_user_company_can_delete_insurances(self):

        Insurance.objects.create(id=5,
                                 name="some insurance!", description="this is an insurance")
        response = self.client.delete('/api/insurance/5')
        self.assertEqual(202, response.status_code)

    def test_8_user_none_copmany_can_delete_insurances(self):

        none_company_user = User.objects.create(
            username="mamad_gholi", password="123456", type=5)
        new_token = Token.objects.create(user=none_company_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        Insurance.objects.create(
            name="some insurance!", description="this is an insurance")

        response = self.client.delete('/api/insurance/1')
        self.assertEqual(403, response.status_code)
