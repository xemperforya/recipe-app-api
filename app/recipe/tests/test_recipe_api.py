from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """
        return recipe detail url
    """
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_tag(user, name = 'main course'):
    """
        create a sample tag
    """
    return Tag.objects.create(user=user, name = name)

def sample_ingredient(user, name = 'cinnamon'):
    """
        create a sample ingredient
    """
    return Ingredient.objects.create(user = user, name = name)


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


    def test_view_recipe_detail(self):
        """
            test viewing a recipe detail
        """
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user = self.user))
        recipe.ingredients.add(sample_ingredient(user = self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)
    
    def test_create_basic_recipe(self):
        """
            test creating a recipe
        """
        payload = {
            'title':'chocolate cheesecake',
            'time_minutes':10,
            'price':5.00
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id = res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """
            test create recipes with tags
        """
        tag1 = sample_tag(self.user, name='vegan')
        tag2 = sample_tag(self.user, name='Dessert')

        payload = {
            'title': 'Avocado lime cake',
            'tags' : [tag1.id, tag2.id],
            'time_minutes': 30,
            'price': 4.00
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id = res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """
            test create recipes with ingredients
        """
        ingredient1 = sample_ingredient(self.user, name='Ginger')
        ingredient2 = sample_ingredient(self.user, name='prawn')

        payload = {
            'title': 'Prawns',
            'ingredients' : [ingredient1.id, ingredient2.id],
            'time_minutes': 30,
            'price': 4.00
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id = res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)