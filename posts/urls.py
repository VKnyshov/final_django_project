from django.urls import path
from .views import PostListView, PostCreateView, PostDeleteView, PostUpdateView

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),  # ✅ Новий ендпойнт

]
