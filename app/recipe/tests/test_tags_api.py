from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsAPITests(TestCase):
    """test the publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """
            test that login is required for retrieving tags
        """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITest(TestCase):
    """test private available apis for tags api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'shantanu@weebprofessional.com',
            'root45'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """
            test the list of tags
        """
        Tag.objects.create(user = self.user, name = 'Vegan')
        Tag.objects.create(user = self.user, name = 'Desert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_tags_limited_to_user(self):
        """
            test that the tags returned are limited to the user
        """
        user_2 = get_user_model().objects.create_user(
            'user_2@weeb.com',
            'root45'
        )

        Tag.objects.create(user = user_2, name = 'Fruity')
        tag = Tag.objects.create(user = self.user, name = 'Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)