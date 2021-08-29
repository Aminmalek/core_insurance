from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


class Insurance(models.Model):
    insurance_type = models.CharField(max_length=150)
    description = models.TextField(max_length=500)

class InsuranceConnector(models.model):
    Insurance = models.OneToOneField(Insurance,on_delete=CASCADE,null=False,blank=False)
    is_accepted_by_company = models.BooleanField(default=False)
    #payment = models.OneToOneField(Payment,on_delete=CASCADE,null=False,blank=False)