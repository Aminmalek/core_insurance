from django.db import models
from authenticate.models import User
from payment.models import InsuranceConnector


class Insured(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, null=False, blank=False)
    insurance = models.ForeignKey(
        InsuranceConnector, on_delete=models.CASCADE, null=True, blank=True)
    supported_insureds = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="supported_insureds")
    bank_account_number = models.IntegerField(null=True, blank=True)
