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
    plans = Plan.objects.count()
    last_plan = Plan.objects.all().order_by('-created')
    last_plan_added = last_plan[0]
    plan_meals = last_plan_added.recipeplan_set.all().order_by('day_name')
    return render(request, "dashboard.html", context={"recipes": recipes, "recipeplans": plans,
                                                      "last_plan_added": last_plan_added, "plan_meals": plan_meals})


@csrf_exempt
def show_recipe_id(request, id):
    if request.method == "GET":
        recipe = Recipe.objects.get(pk=id)
        recipe_ingredients = recipe.ingredients
        recipe_ingredients_split = recipe_ingredients.split(", ")
        return render(request, "app-recipe-details.html", {"id": id, "recipe": recipe,
                                                           "recipe_ingredients_split": recipe_ingredients_split})
    if request.method == "POST":
        id = request.POST.get("id")
        liked_recipe = Recipe.objects.get(pk=id)
        liked_recipe.votes += 1
        liked_recipe.save()
        return HttpResponseRedirect(f"/recipe/{id}/")

from django import forms

@csrf_exempt
def add_recipe(request):
    if request.method == "GET":
        if request.GET.get("msg"):
            msg = "Wypełnij poprawnie wszystkie pola"
            return render(request, "app-add-recipe.html", {"msg":msg})
        else:
            return render(request, "app-add-recipe.html")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        ingredients = request.POST.get("ingredients")
        preparing = request.POST.get("preparing")
        if description == "" or name == "" or preparation_time == "" or ingredients == "" or preparing == "":
            return HttpResponseRedirect("/recipe/add/?msg=wiadomosc")
        else:
            t = Recipe()
            t.name = name
            t.ingredients = ingredients
            t.description = description
            t.preparing = preparing
            t.preparation_time = preparation_time
            t.save()
            return HttpResponseRedirect("/recipe/list")


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

    return render(request, "app-details-schedules.html", context={"recipeplans": recipeplans,"plans": plans,
                                                                  "recipes": recipes_list})


@csrf_exempt
def add_schedule(request):
    if request.method == "GET":
        if request.GET.get("msg"):
            msg = "Wypełnij poprawnie wszystkie pola"
            return render(request, "app-add-schedules.html", {"msg":msg})
        else:
            return render(request, "app-add-schedules.html")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name == "" or description == "":
            return HttpResponseRedirect ("/plan/add/?msg=wiadomosc")
        else:
            x = Plan()
            x.name = name
            x.description = description
            x.save()
            return HttpResponseRedirect (f"/plan/{x.id}/details")


def add_recipe_to_schedule(request):
    return render(request, "app-schedules-meal-recipe.html")

