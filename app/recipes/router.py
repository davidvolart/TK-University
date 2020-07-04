from rest_framework import routers
from recipes.views import RecipeViewSet, IngredientViewSet
from django.urls import path, include

router = routers.SimpleRouter()
router.register('recipes', RecipeViewSet)

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls))
]