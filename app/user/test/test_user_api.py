from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
        Test the user api public
    """
    
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
            Test creating a user with valid payload is successful
        """
        payload = {
            'email':'praveen@weeb.com',
            'name':'lichad',
            'password':'password'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_exists(self):
        """
           Test creating a user that already exists fails
        """
        payload = payload = {
            'email':'praveen@weeb.com',
            'password':'password'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_shot(self):
        """
            Test if password is too short
        """
        payload = {
            'email':'praveen@weeb.com',
            'name':'lichad',
            'password':'ad'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
            test if token generated for user created
        """
        payload = {
            'email':'praveen@weeb.com',
            'name':'lichad',
            'password':'adafhhauhffs'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
            test that is token not generated if credentials not valid
        """
        create_user(email='praveen@weeb.com',password='password')
        payload = {
            'email':'praveen@weeb.com',
            'name':'lichad',
            'password':'wrong'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_user(self):
        """
            test if token not generated if user doesnt exist
        """
        payload = {
            'email':'praveen@weeb.com',
            'name':'lichad',
            'password':'wrong'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_user_missing_field(self):
        """
            test that email and password are required
        """
        payload = {
            'email':'praveen@weeb.com',
            'password':''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

