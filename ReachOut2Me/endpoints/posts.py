from rest_framework import generics, status
from ..models import Post
from rest_framework.response import Response
from ..serializers import PostSerializer


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
        

class PostLikeView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, pk):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            message = 'Unliked post successfully'
        else:
            post.likes.add(user)
            message = 'Liked post successfully'
        post.save()
        serializer = self.get_serializer(post)
        return Response({'post': serializer.data, 'message': message}, status=status.HTTP_200_OK)
