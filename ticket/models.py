from django.db import models
from authenticate.models import User
from payment.models import InsuranceConnector
from insurance.models import Coverage
from django.utils import timezone

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
        max_length=10, choices=TICKET_STATUS_CHOICES, default="Opened")

    def __str__(self):
        return self.name


class ReviewerTimeline(models.Model):
    date = models.DateTimeField(default=timezone.now)
    changed_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    reviewer = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="reviewer")


class Claim(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    insurance = models.ForeignKey(
        InsuranceConnector, on_delete=models.DO_NOTHING,related_name='claims_insurance')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250, null=True,)
    status = models.CharField(max_length=10, choices=CLAIM_STATUS_CHOICES,default="Opened")
    response = models.TextField(max_length=250)
    claim_form = models.JSONField()
    is_archived = models.BooleanField(default=False)
    reviewer = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="claim_reviewer")
    franchise = models.IntegerField(null=True)
    tarrif = models.IntegerField(null=True)
    payable_amount = models.IntegerField(null=True)
    deducations = models.IntegerField(null=True)
    vendor = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, related_name="vendor")
    claimed_amount = models.IntegerField(null=True)
    claim_date = models.DateTimeField(null=True)
    specefic_name = models.CharField(max_length=50)
    coverage = models.ForeignKey(
        Coverage, blank=True, related_name="claim_coverage", on_delete=models.CASCADE)
    reviewer_timeline = models.ManyToManyField(
        ReviewerTimeline, blank=True, related_name="claim_reviewer_time_line_claim")

    def __str__(self):
        return self.description
