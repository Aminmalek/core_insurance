from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authenticate.models import User
from django.urls import reverse
from Core.models import Message


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

    def test_1_user_copmany_post_messages(self):
        User.objects.create(username=87542165,
                            password=6545454, type=1, phone=94578120)
        data = {"message": "this is my message!", "receiver": 87542165}
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)

    def test_2_user_copmany_cant_post_empty_messages(self):
        User.objects.create(username=87542165,
                            password=6545454, type=1, phone=94578120)
        data = None
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_3_user_can_read_recieved_messages(self):
        User.objects.create(username=87542165,
                            password=6545454, type=1, phone=94578120)
        receiver = User.objects.get(username=87542165)
        Message.objects.create(sender=self.user, message="helloooo this is messageeee!!!",
                               receiver=receiver)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_4_user_can_read_his_send_messages(self):
        User.objects.create(username=87542165,
                            password=6545454, type=1, phone=94578120)
        receiver = User.objects.get(username=87542165)
        Message.objects.create(sender=self.user, message="helloooo this is messageeee!!!",
                               receiver=receiver)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_5_user_can_update_his_recieved_messages(self):
        User.objects.create(username=87542165,
                            password=6545454, type=1, phone=94578120)
        sender = User.objects.get(username=87542165)
        Message.objects.create(id=5, sender=sender, message="helloooo this is messageeee!!!",
                               receiver=self.user)
        data = {"response": "this is response!"}
        response = self.client.put('/api/message/5', data)
        self.assertEqual(200, response.status_code)

    def test_6_user_can_update_some_ones_messages(self):
        User.objects.create(username=87542165,
                            password=6545454, type=1, phone=94578120)
        receiver = User.objects.get(username=87542165)
        Message.objects.create(id=6, sender=self.user, message="helloooo this is messageeee!!!",
                               receiver=receiver)
        data = {"response": "this is response!"}
        response = self.client.put('/api/message/6', data)
        self.assertEqual(400, response.status_code)

   
