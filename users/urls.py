from django.contrib import admin
from django.urls import path

from .views import AuthenticatedUser, PermissionAPIView, ProfileInfoAPIView, ProfilePasswordAPIView, RoleViewSet, UserGenericAPIView, logout, register, login

urlpatterns = [
    path("register", register),
    path("login", login),
    path("logout", logout),
    path("user", AuthenticatedUser.as_view()),
    path("permissions", PermissionAPIView.as_view()),
    path("roles", RoleViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path("roles/<str:pk>", RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('user/info', ProfileInfoAPIView.as_view()),
    path('user/password', ProfilePasswordAPIView.as_view()),
    path('users', UserGenericAPIView.as_view()),
    path('users/<str:pk>', UserGenericAPIView.as_view()),
]