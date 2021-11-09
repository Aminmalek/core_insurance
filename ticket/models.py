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
    description = models.TextField(max_length=250, null=True,)
    status = models.CharField(
        max_length=10, choices=TICKET_STATUS_CHOICES, null=True)

    def __str__(self):
        return self.name


class Claim(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    insurance = models.ForeignKey(
        InsuranceConnector, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250, null=True,)
    status = models.CharField(max_length=10, choices=CLAIM_STATUS_CHOICES)
    response = models.TextField(max_length=250)
    claim_form = models.JSONField()
    is_archived = models.BooleanField(default=False)
    reviewer = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True,related_name="reviewer")
    franchise = models.IntegerField(null=True)
    tarrif = models.IntegerField(null=True)
    payable_amount = models.IntegerField(null=True)
    deducations = models.IntegerField(null=True)
    vendor = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True,related_name="vendor")
    claimed_amount = models.IntegerField(null=True)
    claim_date = models.DateTimeField(null=True)
    specefic_name = models.CharField(max_length=50)
    coverage = models.CharField(max_length=40)

    def __str__(self):
        return self.title
