from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import UserProfile
from rest_framework.authtoken.models import Token


class ProfileTestCase(TestCase):
    """This class defines the test suite for the post model."""

    def setUp(self):
        self.url = reverse("user_profile")
        """Define the test client and other test variables."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpasswordForMe",
            first_name="testfirstname",
            last_name="testlastname",
            email="test@email.com",
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_user_profile(self):
        """Test the api can get user profile."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], None)
        self.assertEqual(response.data["user"], self.user.id)

    def test_search_by_username(self):
        """Test the api can get user profile by username."""
        response = self.client.get(
            reverse("search_user", kwargs={"username": "testuser"})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "testfirstname")

    def test_update_user_profile(self):
        """Test the api can update user profile."""
        response = self.client.put(
            self.url,
            data={
                "bio": "test bio",
                "country": "france",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "test bio")
        self.assertEqual(response.data["country"], "france")
        self.assertEqual(response.data["user"], self.user.id)

    def test_get_user_account(self):
        """Test the api can get user account."""
        response = self.client.get(reverse("get_user_profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
