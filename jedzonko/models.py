from django.db import models


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    preparation_time = models.IntegerField(null=True)
    votes = models.IntegerField(default=0)