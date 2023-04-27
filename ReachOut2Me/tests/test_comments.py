from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import UserProfile, Post, Comment
from rest_framework.authtoken.models import Token


class CommentTestCase(TestCase):
    """This class defines the test suite for the post model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="testfirstname",
            last_name="testlastname",
            email="test@email.com"
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword2",
            first_name="testfirstname2",
            last_name="testlastname2",
            email="test2@email.com"
        )
        self.post = Post.objects.create(
            content="test content",
            author=self.user
        )
        self.comment = Comment.objects.create(
            content="test comment",
            author=self.user2,
            post=self.post
        )

        self.url = reverse("create-comment", kwargs={"post_id": self.post.id})
        self.token = Token.objects.create(user=self.user2)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_comment_on_a_post(self):
        """Test the api can get comment on a post."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["content"], "test comment")
        self.assertEqual(response.data[0]["author"], self.user2.username)
        self.assertEqual(response.data[0]["post"], self.post.id)

