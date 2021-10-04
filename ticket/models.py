from django.db import models
from django.db.models.fields import CharField
from authenticate.models import User
from payment.models import InsuranceConnector

CLAIM_STATUS_CHOICES = (
    ('Opened', 'Opened'),
    ('Reopened', 'Reopened'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)

TICKET_STATUS_CHOICES = (
    ('Opened', 'Opened'),
    ('Reopened', 'Reopened'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)


class Ticket(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES)

    def __str__(self):
        return self.name


class Claim(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    insurance = models.ForeignKey(
        InsuranceConnector, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=CLAIM_STATUS_CHOICES)
    response = models.TextField(max_length=500)
    claim_form = models.JSONField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title
