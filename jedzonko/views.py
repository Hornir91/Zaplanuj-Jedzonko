from random import shuffle

from django.shortcuts import render
from django.views import View
from jedzonko.models import *

from django.core.paginator import Paginator

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt




class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        recipes = list(Recipe.objects.all())
        shuffle(recipes)
        recipe0 = recipes[0]
        recipe1 = recipes[1]
        recipe2 = recipes[2]
        return render(request, "index.html", {"ctx": ctx, "recipe0": recipe0, "recipe1": recipe1, "recipe2": recipe2})


def recipes(request):
    recipes = Recipe.objects.all().order_by('-created').order_by('-votes')
    paginator = Paginator(recipes, 50)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request,  "app-recipes.html", context={"recipes": page},)

def dashboard(request):
    recipes = Recipe.objects.count()
    recipeplans = RecipePlan.objects.count()
    return render(request, "dashboard.html", context={"recipes": recipes, "recipeplans": recipeplans})



def show_recipe_id(request, id):
    return render(request, "app-recipe-details.html", {"id": id})

from django import forms

@csrf_exempt
def add_recipe(request):
    if request.method == "GET":
        # msg = request.POST.get("dupa")
        return render(request, "app-add-recipe.html")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        ingredients = request.POST.get("ingredients")
        preparing = request.POST.get("preparing")
        if description == "" or name == "" or preparation_time == "" or ingredients == "" or preparing == "":
            # msg = "dupa"
            # return render (request, "/recipe/add", msg)
            return HttpResponse (f'"Wypełnij poprawnie wszystkie pola"<br><br> <a href="/recipe/add/">wróć do dodawania przepisu</a>')
        else:
            t = Recipe()
            t.name = name
            t.ingredients = ingredients
            t.description = description
            t.preparing = preparing
            t.preparation_time = preparation_time
            t.save()
            return HttpResponseRedirect ("/recipe/list")


def modify_recipe(request, id):
    return render(request, "app-edit-recipe.html", {"id": id})

def schedules(request):
    plans = Plan.objects.all().order_by('name')
    paginator = Paginator(plans, 50)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, "app-schedules.html", context={"plans": page},)

def schedule_details(request, id):
    plans = Plan.objects.get(id=id)
    recipeplans = RecipePlan.objects.filter (id=id)
    recipes = Recipe.objects.filter(recipeplan = id)
    recipes_list = ""
    for recipe in recipes:
        recipes_list += f"{recipe.name}"

    return render(request,"app-details-schedules.html", context={"recipeplans": recipeplans,"plans": plans, "recipes": recipes_list})


@csrf_exempt
def add_schedule(request):
    if request.method == "GET":
        return render(request, "app-add-schedules.html")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        x = Plan()
        x.name = name
        x.description = description
        x.save()
        return HttpResponseRedirect ("/plan/list")


def add_recipe_to_schedule(request):
    return render(request, "app-schedules-meal-recipe.html")

