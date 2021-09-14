from django.db import models

class Ticket(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    is_accepted_by_vendor = models.BooleanField(default=False)
    is_accepted_by_company = models.BooleanField(default=False)
    has_withdrawed = models.BooleanField(default=False)
    