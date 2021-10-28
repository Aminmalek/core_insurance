from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser):
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
    email = models.EmailField(('email address'), blank=True)
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )

    is_superuser = models.BooleanField(
        ('superuser status'),
        default=False,
        help_text=(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
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
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser
    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

       

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'bank_account_number']
    # For Using in django admin panel 
