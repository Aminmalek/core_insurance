from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TYPE_CHOICES = [
        ('Company', 'Company'),
        ('Vendor', 'Vendor'),
        ('Holder', 'Holder'),
        ('SuperHolder', 'SuperHolder'),
        ('Insured', 'Insured'),
    ]
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)
    phone = models.IntegerField()
    def __str__(self):
        return self.username
