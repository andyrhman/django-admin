from django.contrib import admin
from django.urls import path

from .views import AuthenticatedUser, PermissionAPIView, logout, register, login

urlpatterns = [
    path("register", register),
    path("login", login),
    path("logout", logout),
    path("user", AuthenticatedUser.as_view()),
    path("permissions", PermissionAPIView.as_view()),
]