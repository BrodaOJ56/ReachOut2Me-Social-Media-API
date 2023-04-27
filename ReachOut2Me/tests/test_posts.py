from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import UserProfile
from rest_framework.authtoken.models import Token


class PostTestCase(TestCase):
    """This class defines the test suite for the post model."""

    def setUp(self):
        self.url = reverse('post_list_create')
        """Define the test client and other test variables."""
        self.user = User.objects.create_user(username='testuser', password='testpassword',
                                             first_name='testfirstname', last_name='testlastname',
                                             email = 'test@email.com'
                                                )
        UserProfile.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_all_posts(self):
        """Test the api can get all posts."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])

    def test_create_post(self):
        """Test the api can create a post."""
        response = self.client.post(self.url, data={"content": "test content"
                                                    })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'test content')
        self.assertEqual(response.data['author'], self.user.username)
