from django.db import models
from authenticate.models import User

class SuperHolder(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT)
    supported_holders = models.ManyToManyField(
        User, blank=True, related_name="supported_holders")

    def __str__(self):
        return self.user.username
