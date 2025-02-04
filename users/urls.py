from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserDeleteView,
    UserUpdateView,
    UserListView,
    UserSearchView,
    UserFilterView,

)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("delete/", UserDeleteView.as_view(), name="user-delete"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("user/search/", UserSearchView.as_view(), name="user-search"),
    path("user/filter/", UserFilterView.as_view(), name="user-filter"),
]
