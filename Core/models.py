from django.db import models
from authenticate.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    message = models.TextField(max_length=250)
    receiver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="receiver",null=True)
    response = models.TextField(max_length=250)
