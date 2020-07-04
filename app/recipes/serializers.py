from rest_framework import serializers
from recipes import models


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ('name',)
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = models.Recipe
        fields = ('name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.get('ingredients')
        del validated_data['ingredients']
        recipe = models.Recipe.objects.create_recipe(recipe=validated_data, ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        name = validated_data.pop('name', None)
        if name:
            instance.name = name

        description = validated_data.pop('description', None)
        if description:
            instance.description = description

        ingredients_update = validated_data.get('ingredients')
        if ingredients_update:
            instance.delete_ingredients()
            instance.add_ingredients(ingredients_update)

        instance.save()

        return instance