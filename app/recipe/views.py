from os import stat
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
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

    def _params_to_ints(self, qs):
        """
            convert list of string ids into a list of integers
        """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """
            retrive recipes for authenticated user
        """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)
        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """
            return appropriate serializer class
        """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serliazer):
        """
            create new recipe
        """
        serliazer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path = 'upload-image')
    def upload_image(self, request, pk=None):
        """
            upload an image to a recipe
        """
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

