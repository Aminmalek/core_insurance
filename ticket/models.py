from django.db import models
from authenticate.models import User
from payment.models import InsuranceConnector

CLAIM_STATUS_CHOICES = (
    ('Opened', 'Opened'),
    ('Reopened', 'Reopened'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)


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


class Claim(models.Model):
    title = models.CharField(max_length=100)
    insurnace = models.ForeignKey(
        InsuranceConnector, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=CLAIM_STATUS_CHOICES)
    description = models.TextField(max_length=500)
    response = models.TextField(max_length=500)

    def __str__(self):
        return self.title
