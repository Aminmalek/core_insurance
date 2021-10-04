from django.db import models

class Insurance(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=150)
    price = models.IntegerField(null=True)
    register_form = models.JSONField(null=True)
    claim_form = models.JSONField(null=True)

    def __str__(self):
        return self.name
