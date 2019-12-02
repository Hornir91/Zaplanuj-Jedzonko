from django.db import models
from enum import Enum
from datetime import datetime


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.TextField(null=True)
    description = models.TextField(null=True)
    preparing = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField(null=True)
    votes = models.IntegerField(default=0)

class Plan(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")


class DayChoices(Enum):
    Mon = "Monday"
    Tue = "Tuesday"
    Wed = "Wednesday"
    Thu = "Thursday"
    Fri = "Friday"
    Sat = "Saturday"
    Sun = "Sunday"

class DayName(models.Model):
    name = models.CharField(max_length=15, choices=[(tag, tag.value) for tag in DayChoices])

    def __str__(self):
        return f"{self.name}"

class MealNames(Enum):
    Breakfast = "Breakfast"
    Lunch = "Lunch"
    Dinner = "Dinner"
    Tea = "Tea"
    Supper = "Supper"

class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=24, choices=[(tag, tag.value) for tag in MealNames])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.meal_name} {self.recipe} {self.plan} {self.day_name}"

