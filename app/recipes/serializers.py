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

        recipe = models.Recipe(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
        )

        recipe.save()
        ingredients = validated_data.get('ingredients')
        for ingredient in ingredients:
            models.Ingredient.objects.create(recipe=recipe, name=ingredient)

        return recipe

    def update(self, instance, validated_data):

        name = validated_data.pop('name', None)
        if name:
            instance.name = name

        description = validated_data.pop('description', None)
        if description:
            instance.description = description

        instance.save()

        ingredients = models.Ingredient.objects.filter(recipe=instance)
        ingredients.delete()

        ingredients = validated_data.get('ingredients')
        if ingredients:
            for ingredient in ingredients:
                models.Ingredient.objects.create(recipe=instance, **ingredient)

        return instance