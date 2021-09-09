from django.forms import fields
from django.contrib.auth import models

from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id','name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """serializer for ingredients object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipe app"""

    ingredients = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'ingredients',
            'tags', 
            'time_minutes', 
            'price', 
            'link'
        )
        read_only_fields = ('id',)

    

class RecipeDetailSerializer(RecipeSerializer):
    """serializer for recipe details"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only = True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """seriaizer for uploading image"""
    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)