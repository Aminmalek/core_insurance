from insurance.models import Insurance
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField
from authenticate.models import User
from insurance.models import Insurance

class Payment(models.Model):

    user = models.OneToOneField(User, on_delete=CASCADE, null=False, blank=False)
    insurance = models.ForeignKey(Insurance,on_delete=CASCADE)
    is_successfull = models.BooleanField(default=False)
    payment_code = models.IntegerField()