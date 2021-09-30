from django.db import models

TYPE_CHOICES = (
    ('درمانی', 'درمانی'),
)


class Insurance(models.Model):
    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(max_length=150)
    price = models.IntegerField()

    def __str__(self):
        return self.name
