from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from rest_framework.exceptions import NotFound, PermissionDenied


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user']
    ordering_fields = ["created_at"]


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = []
    swagger_fake_view = True

    def get_queryset(self):
        """Swagger вимагає цей метод"""
        return Post.objects.all()

    def get_object(self):
        try:
            post = Post.objects.get(id=self.kwargs["pk"])
        except Post.DoesNotExist:
            raise NotFound({"error": "Пост не знайдено"})

        if post.user != self.request.user:
            raise PermissionDenied({"error": "Ви можете видаляти лише свої пости"})

        return post

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        self.perform_destroy(post)
        return Response({"message": "Пост успішно видалено"}, status=status.HTTP_204_NO_CONTENT)


class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = []
    swagger_fake_view = True

    def get_queryset(self):
        """Swagger вимагає цей метод"""
        return Post.objects.all()

    def get_object(self):
        try:
            post = Post.objects.get(id=self.kwargs["pk"])
        except Post.DoesNotExist:
            raise NotFound({"error": "Пост не знайдено"})

        if post.user != self.request.user:
            raise PermissionDenied({"error": "Ви можете редагувати лише свої пости"})

        return post

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Пост успішно оновлено", "updated_at": self.get_object().updated_at},
                        status=status.HTTP_200_OK)
