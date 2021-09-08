from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers

class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage classes in the db"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
            return objects for the current authenticated user only
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serliazer):
        """
            create new object
        """
        serliazer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the db"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients apis"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """manage RECIPE apis"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
            retrive recipes for authenticated user
        """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """
            return appropriate serializer class
        """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        return self.serializer_class

    def perform_create(self, serliazer):
        """
            create new recipe
        """
        serliazer.save(user=self.request.user)
