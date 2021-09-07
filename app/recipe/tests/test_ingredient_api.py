from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

class PublicIngredientsAPITests(TestCase):
    """tests for ingredients public apis"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
            Test that login is required
        """
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPIClients(TestCase):
    """test case for private ingredients apis"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            'shantanu@weeb.com',
            'root45'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """
            testing a list of ingredients
        """
        Ingredient.objects.create(user = self.user, name = 'Pepper')
        Ingredient.objects.create(user = self.user, name = 'Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredient = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredient, many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """
            test that ingredients returned are limited to the logged in user
        """
        user2 = get_user_model().objects.create_user(
            'praveen@weeb.com',
            'root45'
        )
        Ingredient.objects.create(user=user2, name = 'Turmeric')
        ingredient = Ingredient.objects.create(user = self.user, name = 'vinegar')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """
            test ingredient created successfully
        """
        payload = {
            'name':'Dough'
        }
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user = self.user,
            name = payload['name'],
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_with_ivalid_payload(self):
        """
            test that invalid payload is not allowed
        """
        payload = {
            'name':''
        }
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)