from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser,PermissionsMixin):
    TYPE_CHOICES = [
        ('Company', 'Company'),
        ('Vendor', 'Vendor'),
        ('Holder', 'Holder'),
        ('SuperHolder', 'SuperHolder'),
        ('Insured', 'Insured'),
    ]
    type = models.CharField(max_length=11, choices=TYPE_CHOICES)
    phone = models.BigIntegerField(null=True)
    bank_account_number = models.CharField(max_length=26)
    cash = models.IntegerField(default=0)

    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'), 
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    first_name = models.CharField(('first name'), max_length=150, blank=True)
    last_name = models.CharField(('last name'), max_length=150, blank=True)
    email = models.EmailField(('email address'), blank=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'bank_account_number']

    def __str__(self):
        return self.username
