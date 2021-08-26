from django.forms.fields import EmailField
from django.test import TestCase
from django.contrib.auth import get_user_model


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
        