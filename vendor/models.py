from django.db import models
from django.db.models.deletion import CASCADE
from authenticate.models import User


class Vendor(models.Model):

    user = models.OneToOneField(User,on_delete=CASCADE)
    is_active = models.BooleanField(default=False)
    bank_account_number = models.IntegerField()
