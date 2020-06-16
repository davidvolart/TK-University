from django.test import TestCase
from recipes.models import Recipe, Ingredient


class ModelsTest(TestCase):

    def test_create_ingredients(self):
        """Test that an ingredient is created successfully"""
        recipe = Recipe.objects.create(
            name='Recipe name',
            description='Recipe description'
        )

        ingredient = Ingredient.objects.create(
            name='Ingredient1',
            recipe=recipe
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_create_recipe(self):
        """Test that an recipe is created successfully"""
        recipe = Recipe.objects.create(
            name='Recipe name',
            description='Recipe description'
        )

        self.assertEqual(str(recipe), recipe.name)