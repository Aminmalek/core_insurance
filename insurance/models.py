from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


class Insurance(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=150)
    price = models.IntegerField()

    def __str__(self):
        return self.name
