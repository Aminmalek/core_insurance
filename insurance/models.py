from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


class Insurance(models.Model):
    insurance_type = models.CharField(max_length=150)
    description = models.TextField(max_length=500)

