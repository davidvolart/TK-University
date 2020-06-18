from django.db import models


class RecipeManager(models.Manager):
    """Recipe model manager"""
    def create_recipe(self, recipe, ingredients):
        recipe = self.create(**recipe)
        recipe.add_ingredients(ingredients)
        return recipe


class Recipe(models.Model):
    """Recipe model"""
    name = models.TextField(max_length=255)
    description = models.CharField(max_length=255)

    objects = RecipeManager()

    def add_ingredients(self, ingredients):
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=self, **ingredient)

    def delete_ingredients(self):
        Ingredient.objects.filter(recipe=self).delete()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model"""
    name = models.TextField(max_length=255)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return self.name
