from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, Comment, CommentReply
from rest_framework.authtoken.models import Token


class CommentTestCase(TestCase):
    """This class defines the test suite for the post model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpasswordForMe",
            first_name="testfirstname",
            last_name="testlastname",
            email="test@email.com"
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword2ForUs",
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

        self.reply = CommentReply.objects.create(
            comment=self.comment,
            reply="test reply test",
            user=self.user
        )

        self.url = reverse("create-comment", kwargs={"post_id": self.post.id})
        self.token = Token.objects.create(user=self.user2)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_comment_on_a_post(self):
        """Test the api can get comment on a post."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        # self.assertEqual(response.data[0]["content"], "test comment")
        # self.assertEqual(response.data[0]["author"], self.user2.username)
        # self.assertEqual(response.data[0]["post"], self.post.id)

    # def test_create_comment_on_a_post(self):
    #     """Test the api can create comment on a post."""
    #     data = {
    #         "content": "test comment 2",
    #         "author": self.user2.username,
    #         "post": self.post.id
    #     }
    #     response = self.client.post(self.url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["content"], "test comment 2")
    #     self.assertEqual(response.data["author"], self.user2.username)
    #     self.assertEqual(response.data["post"], self.post.id)
    #
    # def test_update_a_comment_on_a_post(self):
    #     """Test the api can update a comment on a post."""
    #     url = reverse("update-comment", kwargs={"post_id": self.post.id, "comment_id": self.comment.id})
    #     data = {
    #         "content": "test comment updated",
    #         "author": self.user2.username,
    #         "post": self.post.id
    #     }
    #     response = self.client.put(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["content"], "test comment updated")
    #     self.assertEqual(response.data["author"], self.user2.username)
    #     self.assertEqual(response.data["post"], self.post.id)
    #
    # def test_create_comment_reply(self):
    #     """Test the api can reply to a comment on a post."""
    #     url = reverse("create_get_comment_reply",
    #                   kwargs={"comment_id": self.comment.id})
    #     data = {
    #         "comment": self.comment.id,
    #         "reply": "test comment reply",
    #         "user": self.user2.id
    #     }
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["comment"], self.comment.id)
    #     self.assertEqual(response.data["reply"], "test comment reply")
    #     self.assertEqual(response.data["user"], self.user2.id)
    #
    # def test_update_comment_reply(self):
    #     """Test the api can update a reply to a comment on a post."""
    #     url = reverse("update_delete_comment_reply",
    #                   kwargs={"comment_id": self.comment.id, "reply_id": self.reply.id})
    #     data = {
    #         "comment": self.comment.id,
    #         "reply": "test comment reply updated",
    #         "user": self.user2.id
    #     }
    #     response = self.client.put(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["comment"], self.comment.id)
    #     self.assertEqual(response.data["reply"], "test comment reply updated")
    #     self.assertEqual(response.data["user"], self.user2.id)
    #
    # def test_delete_comment_reply(self):
    #     """Test the api can delete a reply to a comment on a post."""
    #     url = reverse("update_delete_comment_reply",
    #                   kwargs={"comment_id": self.comment.id, "reply_id": self.reply.id})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data["message"], "Comment reply deleted successfully.")
