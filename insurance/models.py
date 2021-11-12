from django.db import models
from django.db.models.fields import IntegerField

# price field most change

class Coverage(models.Model):
    name = models.CharField(max_length=50)
    claim_form = models.JSONField(null=True)
    capacity = IntegerField()

    def __str__(self):
        return self.name
        
class Insurance(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=150)
    price = models.IntegerField(null=True)
    register_form = models.JSONField(null=True)
    coverage = models.ManyToManyField(Coverage,blank=True,related_name="coverage")
    
    def __str__(self):
        return self.name

