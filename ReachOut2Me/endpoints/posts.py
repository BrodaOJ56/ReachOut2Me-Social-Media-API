from rest_framework import generics, status
from ..models import Post, Comment, CommentReply
from rest_framework.response import Response
from ..serializers import PostSerializer, CommentSerializer, CommentReplySerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_destroy(self, instance):
        instance.delete()
        

# the class below is used to like/unlike a post
# the generic.GenericAPIView class is used to create a custom view
class PostLikeView(generics.GenericAPIView):
    # the queryset attribute is used to retrieve the post object
    queryset = Post.objects.all()
    # the serializer_class attribute is used to serialize the post object
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
        # the save method is used to save the changes to the post object
        post.save()
        # the get_serializer method is used to serialize the post object
        serializer = self.get_serializer(post)
        # the Response method is used to send a response to the user
        return Response({'post': serializer.data, 'message': message}, status=status.HTTP_200_OK)


class CreateComment(APIView):
    pass


class CreateGetComment(APIView):
    serializer_class = CommentSerializer

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(post=post)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateDeleteComment(APIView):
    serializer_class = CommentSerializer

    def put(self, request, post_id, comment_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = Comment.objects.get(id=comment_id, post=post)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = Comment.objects.get(id=comment_id, post=post)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    


class ListCreateCommentReply(APIView):
    serializer_class = CommentReplySerializer

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(comment=comment, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        replies = CommentReply.objects.filter(comment=comment)
        serializer = self.serializer_class(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateDeleteCommentReply(APIView):
    serializer_class = CommentReplySerializer

    def put(self, request, comment_id, reply_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            reply = CommentReply.objects.get(id=reply_id, comment=comment)
        except CommentReply.DoesNotExist:
            return Response({'error': 'Comment reply not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(reply, data=request.data, context={'request': request, 'comment_id': comment_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id, reply_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            reply = CommentReply.objects.get(id=reply_id, comment=comment)
        except CommentReply.DoesNotExist:
            return Response({'error': 'Comment reply not found.'}, status=status.HTTP_404_NOT_FOUND)

        reply.delete()
        return Response({'message': 'Comment reply deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
class CommentLike(APIView):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.likes.add(request.user)
        return Response({'message': 'Comment liked successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.likes.remove(request.user)
        return Response({'message': 'Comment unliked successfully.'}, status=status.HTTP_200_OK)