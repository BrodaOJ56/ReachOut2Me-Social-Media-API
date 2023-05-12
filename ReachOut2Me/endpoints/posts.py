from rest_framework import generics, status
from ..models import Post, Comment, CommentReply, CommentReplyLike, Notification
from rest_framework.response import Response
from ..serializers import PostSerializer, CommentSerializer, CommentReplySerializer, CommentReplyLikeSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from django.contrib.contenttypes.models import ContentType

@extend_schema(
        tags=['Post']
    )
class PostListCreateView(generics.ListCreateAPIView):
    """
    The `queryset` attribute defines the list of posts to be displayed,
    while the `serializer_class` attribute determines how the data is serialized and deserialized.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    """    
    The `perform_create` method is used to save the post object with the authenticated user as the author. 
    This ensures that the author of the post is properly associated with it in the database.
    """

    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# The PostDetailView class is a generic view that retrieves, updates, or deletes a Post instance
@extend_schema(
        tags=['Post']
    )
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Set the queryset attribute to retrieve all Post instances
    queryset = Post.objects.all()
    # Set the serializer_class attribute to PostSerializer
    serializer_class = PostSerializer

    # Define the perform_destroy method to delete a Post instance
   
    def perform_destroy(self, instance):
        instance.delete()

    # Define the put method to update a Post instance
    def put(self, request, *args, **kwargs):
        # Retrieve the Post instance using the pk value from the URL
        post = Post.objects.get(id=kwargs['pk'])
        # Instantiate a PostSerializer with the Post instance and request data
        serializer = PostSerializer(post, data=request.data)
        # Validate the serializer data
        if serializer.is_valid():
            # Check if the user is the author of the post
            if request.user == post.author:
                # Save the updated Post instance
                serializer.save()
                # Return the updated Post instance with a 200 OK status code
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Return an error message if the user is not the author with a 403 Forbidden status code
                return Response({'error': 'You are not the author of this post.'}, status=status.HTTP_403_FORBIDDEN)


# The PostLikeView class is a custom view to like or unlike a Post instance
@extend_schema(
        tags=['Post']
    )
class PostLikeView(generics.GenericAPIView):
    # Set the queryset attribute to retrieve all Post instances
    queryset = Post.objects.all()
    # Set the serializer_class attribute to PostSerializer
    serializer_class = PostSerializer

    
    def post(self, request, pk):
        # the get_object method is used to retrieve the post object using the pk from the url
        # the pk is passed to the get_object method as an argument
        post = self.get_object()
        # the request.user attribute is used to retrieve the user object from the request
        user = request.user
        # if the user object is in the post.likes.all() queryset, the user has already liked the post
        if user in post.likes.all():
            # the remove method is used to remove the user object from the post.likes.all() queryset
            post.likes.remove(user)
            # the message variable is used to send a message to the user
            message = 'Unliked post successfully'
        # if the user object is not in the post.likes.all() queryset, the user has not liked the post
        else:
            # the add method is used to add the user object to the post.likes.all() queryset
            post.likes.add(user)
            # the message variable is used to send a message to the user
            message = 'Liked post successfully'

            # Create notification for post creator
            recipient = post.user
            actor = user
            notification_type = 'post_like'
            Notification.objects.create(
                recipient=recipient,
                actor_content_type=ContentType.objects.get_for_model(actor),
                actor_object_id=actor.id,
                verb=notification_type,
                actor_object=post
            )
        # the save method is used to save the changes to the post object
        post.save()
        # the get_serializer method is used to serialize the post object
        serializer = self.get_serializer(post)
        # the Response method is used to send a response to the user
        return Response({'post': serializer.data, 'message': message}, status=status.HTTP_200_OK)


# view to create and get comments
@extend_schema(
        tags=['Comment']
    )
class CreateGetComment(APIView):
    # set the serializer_class attribute to CommentSerializer
    serializer_class = CommentSerializer

    # the post method is used to create a comment
    # the post_id argument is used to retrieve the post object
    # the request argument is used to retrieve the request object
    
    def post(self, request, post_id):
        # the try block is used to retrieve the post object using the post_id argument
        try:
            post = Post.objects.get(id=post_id)
        # the except block is used to return an error message if the post object does not exist
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the serializer_class attribute is used to instantiate a CommentSerializer object
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # the is_valid method is used to validate the serializer data
        # if the data is valid, the save method is used to save the comment object
        if serializer.is_valid():
            serializer.save(post=post)

                # create a notification object for the post owner
            recipient = post.user
            actor = request.user
            verb = 'comment'
            Notification.objects.create(recipient=recipient, 
                                        actor_object=post,
                                        verb=verb, 
                                        actor_content_type=ContentType.objects.get_for_model(actor))

            # the Response method is used to send a response to the user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if the data is not valid, the errors are returned with a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # the get method is used to retrieve all comments for a post
    def get(self, request, post_id):
        # the try block is used to retrieve the post object using the post_id argument
        try:
            post = Post.objects.get(id=post_id)
        # the except block is used to return an error message if the post object does not exist
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the filter method is used to retrieve all comments for the post object
        comments = Comment.objects.filter(post=post)
        # the serializer_class attribute is used to instantiate a CommentSerializer object
        # the many argument is set to True to serialize multiple objects
        serializer = self.serializer_class(comments, many=True)
        # the Response method is used to send a response to the user
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# view to update and delete comments
@extend_schema(
        tags=['Comment']
    )
class UpdateDeleteComment(APIView):
    # set the serializer_class attribute to CommentSerializer
    serializer_class = CommentSerializer

    
    def put(self, request, post_id, comment_id):
        # the try block is used to retrieve the post object using the post_id argument
        try:
            post = Post.objects.get(id=post_id)
        # the except block is used to return an error message if the post object does not exist
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the try block is used to retrieve the comment object using the comment_id argument
        try:
            comment = Comment.objects.get(id=comment_id, post=post)
        # the except block is used to return an error message if the comment object does not exist
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the serializer_class attribute is used to instantiate a CommentSerializer object
        serializer = self.serializer_class(comment, data=request.data, context={'request': request})
        # if the data is valid, the save method is used to save the comment object
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # if the data is not valid, the errors are returned with a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # the delete method is used to delete a comment
    def delete(self, request, post_id, comment_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = Comment.objects.get(id=comment_id, post=post)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # delete the comment object
        comment.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# view to create and get comment replies
@extend_schema(
        tags=['Comment']
    )
class ListCreateCommentReply(APIView):
    # set the serializer_class attribute to CommentReplySerializer
    serializer_class = CommentReplySerializer

    # the post method is used to create a comment reply
    
    def post(self, request, comment_id):
        # the try block is used to retrieve the comment object using the comment_id argument
        try:
            comment = Comment.objects.get(id=comment_id)
        # the except block is used to return an error message if the comment object does not exist
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the serializer_class attribute is used to instantiate a CommentReplySerializer object
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # if the data is valid, the save method is used to save the comment reply object
        if serializer.is_valid():
            serializer.save(comment=comment, user=request.user)

            # create a notification object for the recipient
            recipient = comment.user
            actor = request.user
            verb = "reply"
            actor_content_type = ContentType.objects.get_for_model(actor)
            Notification.objects.create(recipient=recipient,
                                                        actor_content_type=actor_content_type, 
                                                        actor_object_id=actor.id, 
                                                    verb=verb, 
                                                    actor_object=comment.post)
            # the Response method is used to send a response to the user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if the data is not valid, the errors are returned with a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # the get method is used to retrieve all comment replies for a comment
    
    def get(self, request, comment_id):
        # the try block is used to retrieve the comment object using the comment_id argument
        try:
            comment = Comment.objects.get(id=comment_id)
        # the except block is used to return an error message if the comment object does not exist
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the filter method is used to retrieve all comment replies for the comment object
        replies = CommentReply.objects.filter(comment=comment)
        # the serializer_class attribute is used to instantiate a CommentReplySerializer object
        # the many argument is set to True to serialize multiple objects
        serializer = self.serializer_class(replies, many=True)
        # the Response method is used to send a response to the user
        return Response(serializer.data, status=status.HTTP_200_OK)


# view to update and delete comment replies
@extend_schema(
        tags=['Comment']
    )
class UpdateDeleteCommentReply(APIView):
    # set the serializer_class attribute to CommentReplySerializer
    serializer_class = CommentReplySerializer

    
    # the put method is used to update a comment reply
    def put(self, request, comment_id, reply_id):
        # the try block is used to retrieve the comment object using the comment_id argument
        try:
            comment = Comment.objects.get(id=comment_id)
        # the except block is used to return an error message if the comment object does not exist
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the try block is used to retrieve the comment reply object using the reply_id argument
        try:
            reply = CommentReply.objects.get(id=reply_id, comment=comment)
        # the except block is used to return an error message if the comment reply object does not exist
        except CommentReply.DoesNotExist:
            return Response({'error': 'Comment reply not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the serializer_class attribute is used to instantiate a CommentReplySerializer object
        serializer = self.serializer_class(reply, data=request.data, context={'request': request, 'comment_id': comment_id})
        # if the data is valid, the save method is used to save the comment reply object
        if serializer.is_valid():
            serializer.save()
            # the Response method is used to send a response to the user
            return Response(serializer.data, status=status.HTTP_200_OK)
        # if the data is not valid, the errors are returned with a 400 Bad Request status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # the delete method is used to delete a comment reply
    def delete(self, request, comment_id, reply_id):
        # the try block is used to retrieve the comment object using the comment_id argument
        try:
            comment = Comment.objects.get(id=comment_id)
        # the except block is used to return an error message if the comment object does not exist
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the try block is used to retrieve the comment reply object using the reply_id argument
        try:
            reply = CommentReply.objects.get(id=reply_id, comment=comment)
        # the except block is used to return an error message if the comment reply object does not exist
        except CommentReply.DoesNotExist:
            return Response({'error': 'Comment reply not found.'}, status=status.HTTP_404_NOT_FOUND)

        # the delete method is used to delete the comment reply object
        reply.delete()
        # the Response method is used to send a response to the user
        return Response({'message': 'Comment reply deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(request=CommentReplyLikeSerializer,
        responses={204: None},
        tags=['Comment']
    )
class CommentReplyLikeView(APIView):
    def post(self, request, comment_reply_id):
        # Get the comment reply object by its ID
        try:
            comment_reply = CommentReply.objects.get(pk=comment_reply_id)
        except CommentReply.DoesNotExist:
            # If the comment reply does not exist, return a 404 error
            return Response({"message": "Comment reply not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create a new comment reply like object for the current user and the given comment reply
        comment_reply_like, created = CommentReplyLike.objects.get_or_create(
            comment_reply=comment_reply, user=request.user)
        
        # Serialize and return the comment reply like object
        serializer = CommentReplyLikeSerializer(comment_reply_like)

        # Get the recipient user
        recipient = comment_reply.user

        # Get the actor user
        actor = request.user

        # Create the notification object
        notification = Notification(
            recipient=recipient,
            actor_object_id=actor.id,
            actor_content_type=ContentType.objects.get_for_model(actor),
            verb='liked your comment reply',
            actor_object=comment_reply,
        )

        # Save the notification object to the database
        notification.save()


        # If the comment reply like object was not created (meaning the user has already liked the comment reply), return a 400 error
        if not created:
            return Response({"message": "You have already liked this comment reply."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the comment reply like object
        serializer = CommentReplyLikeSerializer(comment_reply_like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def delete(self, request, comment_reply_id):
        # Get the comment reply object by its ID
        try:
            comment_reply = CommentReply.objects.get(pk=comment_reply_id)
        except CommentReply.DoesNotExist:
            # If the comment reply does not exist, return a 404 error
            return Response({"message": "Comment reply not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the comment reply like object for the current user and the given comment reply
        comment_reply_like = CommentReplyLike.objects.filter(
            comment_reply=comment_reply, user=request.user)

        # If the comment reply like object does not exist (meaning the user has not liked the comment reply), return a 400 error
        if not comment_reply_like.exists():
            return Response({"message": "You have not liked this comment reply."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the comment reply like object
        comment_reply_like.delete()

        # Return a success message
        return Response({"message": "You have unliked this comment reply."}, status=status.HTTP_200_OK)

    
@extend_schema(
        tags=['Comment'],
        request=None,
        responses={200: CommentSerializer}
    )
class CommentLike(APIView):
    def post(self, request, comment_id):
        # query the Comment model to retrieve a comment object using the comment_id argument
        comment = get_object_or_404(Comment, id=comment_id)
        # add the user to the likes field of the comment object
        comment.likes.add(request.user)
        # Create the notification object
        recipient = comment.user
        actor = request.user
        verb = 'liked your comment'
        actor_content_type = ContentType.objects.get_for_model(actor)
        Notification.objects.create(
            recipient=recipient,
            actor_object_id=actor.id,
            actor_content_type=actor_content_type,
            verb=verb,
            actor_object=comment,
        )
        # serialize the comment object and return the serialized data
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, comment_id):
        # query the Comment model to retrieve a comment object using the comment_id argument
        comment = get_object_or_404(Comment, id=comment_id)
        # remove the user from the likes field of the comment object
        comment.likes.remove(request.user)
        # serialize the comment object and return the serialized data
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)