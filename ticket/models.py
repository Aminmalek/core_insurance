from django.db import models
from authenticate.models import User



class Ticket(models.Model):

    name = models.CharField(max_length=150)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(max_length=500)
    is_accepted_by_vendor = models.BooleanField(default=False)
    is_accepted_by_company = models.BooleanField(default=False)
    has_withdrawed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
