from datetime import datetime

from django.shortcuts import render
from django.views import View
from jedzonko.models import *

from django.core.paginator import Paginator

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt



class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)


def recipes(request):
    recipes = Recipe.objects.all().order_by('-created').order_by('-votes')
    paginator = Paginator(recipes, 50)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request,  "app-recipes.html", context={"recipes": page},)

def dashboard(request):

    recipes = Recipe.objects.count()

    recipeplans = RecipePlan.objects.count()
    return render(request, "dashboard.html", context={"recipes": recipes,"recipeplans":recipeplans,})



def show_recipe_id(request, id):
    return render(request, "app-recipe-details.html", {"id": id})

@csrf_exempt
def add_recipe(request):
    if request.method == "GET":
        return render(request, "app-add-recipe.html")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        ingredients = request.POST.get("ingredients")
        preparing = request.POST.get("preparing")
        t = Recipe()
        t.name = name
        t.ingredients = ingredients
        t.description = description
        t.preparing = preparing
        t.preparation_time = preparation_time
        t.save()
        return HttpResponseRedirect ("/recipe/add")


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

