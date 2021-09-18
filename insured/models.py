from django.db import models
from authenticate.models import User


class Insured(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, null=False, blank=False)
    supported_insureds = models.ManyToManyField(
        User, blank=True, related_name="supported_insureds")
    bank_account_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username
