from django.db import models
from authenticate.models import User
from insurance.models import Insurance


class InsuranceConnector(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insurance = models.ForeignKey(
        Insurance, on_delete=models.CASCADE, null=True, blank=True)
    is_accepted_by_company = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    payment_code = models.IntegerField(null=True, blank=True)
    register_form = models.JSONField()

    def __str__(self):
        return self.insurance.name
