from django.shortcuts import render
from rest_framework import viewsets
from .models import Recipe, Ingredient
from recipes import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage Recipe in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        recipe_name = self.request.query_params.get('name')
        queryset = self.queryset

        if recipe_name:
            queryset = queryset.filter(name__istartswith=recipe_name)

        return queryset


class IngredientViewSet(viewsets.ModelViewSet):
    """Manage Ingredient in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
