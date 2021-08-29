from django.db import models
from django.db.models.deletion import CASCADE
from authenticate.models import User
from insurance.models import Insurance

class Insured(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT,null=False,blank=False)
    insurance = models.ForeignKey(Insurance,on_delete=CASCADE)
    is_holder = models.BooleanField(default=False)
    supported_insureds = models.ForeignKey(User,on_delete=CASCADE,null=True,blank=True)
    bank_account_number = models.IntegerField(max_length=150)
