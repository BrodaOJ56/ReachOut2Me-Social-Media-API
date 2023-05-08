from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post
from rest_framework.authtoken.models import Token


class PostTestCase(TestCase):
    """This class defines the test suite for the post model."""

    def setUp(self):
        self.url = reverse("post_list_create")
        """Define the test client and other test variables."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpasswordForUs",
            first_name="testfirstname",
            last_name="testlastname",
            email="test@email.com",
        )
        self.token = Token.objects.create(user=self.user)
        Post.objects.create(author=self.user, content="test content")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_all_posts(self):
        """Test the api can get all posts."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

#     def test_create_post(self):
#         """Test the api can create a post."""
#         response = self.client.post(self.url, data={"content": "test content"})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["content"], "test content")
#         self.assertEqual(response.data["author"], self.user.username)
#
#     def test_get_a_post_by_id(self):
#         """Test the api can get a post by id."""
#         url = reverse("post_detail", kwargs={"pk": 1})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["content"], "test content")
#         self.assertEqual(response.data["author"], self.user.username)
#
#     def test_delete_a_post_by_id(self):
#         """Test the api can delete a post by id."""
#         url = reverse("post_detail", kwargs={"pk": 1})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Post.objects.count(), 0)
#
#     def test_update_a_post_by_id(self):
#         """Test the api can update a post by id"""
#         url = reverse("post_detail", kwargs={"pk": 1})
#         response = self.client.put(url, data={"content": "test content updated"})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["content"], "test content updated")
#         self.assertEqual(response.data["author"], self.user.username)
