from django.db import models
from django.db.models.deletion import CASCADE
from authenticate.models import User
from insurance.models import Insurance


class InsuranceConnector(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    insurance = models.ForeignKey(
        Insurance, on_delete=CASCADE, null=False, blank=False)
    is_accepted_by_company = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    payment_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.insurance.name
