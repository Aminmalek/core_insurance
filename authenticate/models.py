from django.db import models
from django.contrib.auth.models import AbstractUser


class Type (models.Model):

    COMPANY = 'CO'
    INSURED = 'IN'
    VENDOR = "VE"
    HOLDER = "HO"
    TYPE_CHOICES = [
        (COMPANY, 'Company'),
        (HOLDER, 'Holder'),
        (INSURED, 'Insured'),
        (VENDOR, 'Vendor'),
    ]

    type_name = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=INSURED
    )


class User(AbstractUser):

    user_type = models.OneToOneField(
        Type, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.username
