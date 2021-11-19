from django.db import models
from django.db.models.fields import IntegerField


class Coverage(models.Model):
    name = models.CharField(max_length=100)
    claim_form = models.JSONField(null=True)
    capacity = IntegerField()

    def __str__(self):
        return self.name


class Insurance(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=150, null=True)
    price = models.IntegerField()
    register_form = models.JSONField(null=True)
    coverage = models.ManyToManyField(Coverage, related_name="coverage")

    def __str__(self):
        return self.name
