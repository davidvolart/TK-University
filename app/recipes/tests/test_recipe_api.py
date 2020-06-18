from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from recipes.models import Recipe, Ingredient
from recipes.serializers import RecipeSerializer
from django.urls import reverse

RECIPES_URL = reverse('recipes:recipe-list')


def sample_recipe(**params):
    """Create and return a simple recipe"""
    default = {
        'name': 'Sample recipe',
        'description': 'Nice description',
    }
    default.update(params)

    return Recipe.objects.create(**default)


def get_recipe_detail_url(recipe_id):
    """Return the recipe detail url"""
    return reverse('recipes:recipe-detail', args=[recipe_id])


class PublicRecipeApiTest(TestCase):
    """Test recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieves_recipes(self):
        """Test retrieving a list of recipes"""

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieves_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe()
        sample_recipe()

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_adding_an_invalid_recipe(self):
        """Test adding an invalid recipe"""

        payload = {
            'name': 'Recipe name',
        }

        res = self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_adding_a_recipe(self):
        """Test adding a recipe successfully"""

        payload = {
            "name": "Recipe name",
            "description": "recipe description",
            "ingredients": [{
                'name': 'ingredient1'
            }],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_adding_a_recipe(self):
        """Test adding a recipe successfully"""

        payload = {
            "name": "Recipe name",
            "description": "recipe description",
            "ingredients": [{
                'name': 'ingredient1'
            }],
        }

        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieving_a_detail_recipe(self):
        """Test retrieving a recipe successfully"""

        recipe = Recipe.objects.create(name='Recipe name', description='description recipe')

        res = self.client.get(get_recipe_detail_url(recipe.id))
        serializer = RecipeSerializer(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], serializer.data['name'])
        self.assertEqual(res.data['description'], serializer.data['description'])
        self.assertEqual(len(res.data['ingredients']), len(serializer.data['ingredients']))

    def test_deleting_a_recipe(self):
        """Test deleting a recipe successfully"""

        recipe = Recipe.objects.create(name='Recipe to be delete', description='description recipe')
        Ingredient.objects.create(name='Ingredient1', recipe=recipe)

        res = self.client.delete(get_recipe_detail_url(recipe.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Recipe.objects.filter(id=recipe.id).exists()
        self.assertFalse(exists)
        self.assertEqual(len(Ingredient.objects.all()), 0)

    def test_partial_update_recipe(self):
        """Test partial update for a recipe"""

        recipe_data = {
            'name': 'Recipe to be updated',
            'description': 'description recipe'
        }

        ingredients_data = {
            'name': 'Ingredient1'
        }

        recipe = Recipe.objects.create_recipe(recipe=recipe_data, ingredients=[ingredients_data])

        patch_url = get_recipe_detail_url(recipe.id)

        payload = {
            'name': 'Recipe updated',
            'description': 'New description'
        }

        res = self.client.patch(patch_url, payload)
        recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], recipe.name)
        self.assertEqual(res.data['description'], recipe.description)
        self.assertTrue(Ingredient.objects.filter(name=ingredients_data['name']).exists())
        self.assertEqual(res.data['ingredients'], [ingredients_data])