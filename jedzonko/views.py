from datetime import datetime

from django.shortcuts import render
from django.views import View
from jedzonko.models import *


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


def recipes(request):
    return render(request, "app-recipes.html")

def dashboard(request):

    recipes = Recipe.objects.count()
    return render(request, "dashboard.html", context={"recipes": recipes,})


def show_recipe_id(request, id):
    return render(request, "app-recipe-details.html", {"id": id})

def add_recipe(request):
    return render(request, "app-add-recipe.html")

def modify_recipe(request, id):
    return render(request, "app-edit-recipe.html", {"id": id})

def schedules(request):
    return render(request, "app-schedules.html")

def schedule_details(request, id):
    return render(request, "app-details-schedules.html", {"id": id})

def add_schedule(request):
    return render(request, "app-add-schedules.html")

def add_recipe_to_schedule(request):
    return render(request, "app-schedules-meal-recipe.html")

