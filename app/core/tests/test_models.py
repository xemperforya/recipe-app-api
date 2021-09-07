from django.forms.fields import EmailField
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='shantanu@weeb.com',password='password'):
    """
        create sample user
    """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        """
            Test creating a new user with email and password
        """
        email = 'shantanu@googly.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(email,user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """
            test the email for new user is normalised
        """

        email = 'shantanu@GOOGLY.COM'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(email.lower(),user.email)

    def test_new_user_invalid_email(self):
        """
            test if new user is created with valid email
        """

        with self.assertRaises(ValueError):
            email = None
            password = 'password'
            user = get_user_model().objects.create_user(
                email=email,
                password=password
            )

    def test_superuser_created(self):
        """
        Test if superuser is created
        """
        email = 'Shantanu@gmail.com'
        password = 'password'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """
            test the tag string representation
        """
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """
            test the ingredient string representation
        """
        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = 'Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """
            test the recipe app creation
        """
        recipe = models.Recipe.objects.create(
            user =sample_user(),
            title = 'Steak ad mushroom sauce',
            time_minutes = 5,
            price = 5.00
        )

        self.assertEqual(str(recipe), recipe.title)