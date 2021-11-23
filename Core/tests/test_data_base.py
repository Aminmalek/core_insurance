from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from django.urls import reverse
from insurance.models import Insurance, Coverage
import random
import string
import sys
from time import sleep


class CoreTests(APITestCase):

    def setUp(self):
        self.username = "54872154"
        self.password = "123456"
        self.type = 1
        self.phone = 9128754652
        self.user = User.objects.create(
            username=self.username, password=self.password, type=self.type, phone=self.phone)
        self.url = reverse("message")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user(self):
        user_numbers = 10000

        for a in range(1, user_numbers):

            sys.stdout.write('\r')
            # the exact output you're looking for:
            j = (a + 1) / user_numbers
            sys.stdout.write("[%-20s] %d%%" % ('='*int(20*j), 100*j))
            sys.stdout.flush()
            #sleep(0.25)
            name = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=20))
            password = "123456"
            type = random.randrange(1, 6)
            phone = random.randint(100000000000, 999999999999)
            bank_account_number = random.randint(
                10000000000000000, 99999999999999999)
            user = User.objects.create_user(username=name, password=password, first_name=name,
                                            last_name=name, phone=phone, type=type, bank_account_number=bank_account_number)
            token = Token.objects.create(user=user)

        User.objects.create_user(id=5, username="475274524752", password="654654", first_name="amin",
                                 last_name="malek", phone=964215618515, type=5, bank_account_number=878454876546546574654)
        User.objects.create_user(id=5, username="45445452", password="654654", first_name="amin",
                                 last_name="malek", phone=94215184515, type=5, bank_account_number=878454876546546574654)

        a = User.objects.filter(username="475274524752").explain(
            verbose=True, analyze=True)
        d = User.objects.filter(phone="94215184515").explain(
            verbose=True, analyze=True)
        b = User.objects.filter(type=5).explain(verbose=True, analyze=True)
        c = User.objects.all().explain(verbose=True, analyze=True)
        f = open("queries_explain.txt", "w")

        f.write(str(a)+"\n\n")
        f.write(str(d)+"\n\n")
        f.write(str(b)+"\n\n")
        f.write(str(c)+"\n\n")
        count = len(str(c))/2
        f.write("*"*int(count))
        f.close()

    def test_insurance(self):

        for a in range(1, 1001):
            name = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=30))
            description = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=30))
            price = random.randrange(100000, 1000000)
            register_form = {"name": "some form is it"}
            coverage = Coverage.objects.create(name="coverage1", claim_form=[
                {"name": "name1", "type": "type1"}], capacity=120000)
            insurance = Insurance.objects.create(
                name=name, description=description, price=price)
            insurance.coverage.add(coverage)

        insurance_all = Insurance.objects.all().explain(verbose=True, analyze=True)
        inurance_by_id = Insurance.objects.filter(
            id=7).explain(verbose=True, analyze=True)
        f = open("insurance_queries_explain.txt", "w")
        f.write(str(insurance_all)+"\n\n")
        f.write(str(inurance_by_id)+"\n\n")
        count = len(str(inurance_by_id))/2
        f.write("*"*int(count))
        f.close()
