from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserTestCase(TestCase):
    """This class defines the test suite for the post model."""

    def setUp(self):
        self.url = reverse("get_all_users")
        """Define the test client and other test variables."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="testfirstname",
            last_name="testlastname",
            email="testemail@email.com",
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_all_users(self):
        """Test the api can get all users."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        """Test the api can register users"""
        url = reverse("rest_name_register")
        data = {
              "username": "string001",
              "email": "user@example.com",
              "password1": "Manchester100",
              "password2": "Manchester100",
              "first_name": "stringy",
              "last_name": "string"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
