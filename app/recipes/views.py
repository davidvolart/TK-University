from django.shortcuts import render
from rest_framework import viewsets
from recipes.models import Recipe, Ingredient
from recipes import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage Recipe in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        ingredient_name = self.request.query_params.get('name')
        queryset = self.queryset

        if ingredient_name:
            queryset = queryset.filter(name=ingredient_name)

        return queryset


class IngredientViewSet(viewsets.ModelViewSet):
    """Manage Ingredient in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
