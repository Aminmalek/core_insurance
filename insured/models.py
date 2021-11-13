from insurance.models import Insurance
from django.db import models
from authenticate.models import User


class Insured(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT)
    supported_insureds = models.ManyToManyField(
        User, blank=True, related_name="supported_insureds")
    age = models.SmallIntegerField(null=True)
    illness = models.TextField(max_length=300,null=True)
    
    def __str__(self):
        return self.user.username
