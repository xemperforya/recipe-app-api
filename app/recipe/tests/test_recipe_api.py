from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """
        create and return a sample recipe
    """
    defaults = {
        'title':'sample recipe',
        'time_minutes':10,
        'price':30.00
    }
    defaults.update(params)

    return Recipe.objects.create(user = user, **defaults)


class PublicRecipeAPITest(TestCase):
    """class to test public recipe apis"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
            test authentication is required
        """
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipAPITest(TestCase):
    """Test private apis for recipe api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'shantanu@dweeb.com',
            'root45'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """
            test retrieving recipe list
        """
        sample_recipe(user = self.user)
        sample_recipe(user = self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """
            test that recipes are limited to the user
        """

        user_2 = get_user_model().objects.create_user(
            'weeby@weeby.com',
            'passw1234'
        ) 
        sample_recipe(user = user_2)
        sample_recipe(user = self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)