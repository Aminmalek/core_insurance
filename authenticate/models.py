from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TYPE_CHOICES = [
        ('Company', 'Company'),
        ('Vendor', 'Vendor'),
        ('Holder', 'Holder'),
        ('Insured', 'Insured'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.username
