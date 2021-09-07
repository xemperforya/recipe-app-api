from django.contrib.auth import models

from rest_framework import serializers

from core.models import Tag, Ingredient


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
