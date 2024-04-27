from django.contrib import admin
from django.urls import path

from .views import AuthenticatedUser, logout, users, register, login

urlpatterns = [
    path("users", users),
    path("register", register),
    path("login", login),
    path("logout", logout),
    path("user", AuthenticatedUser.as_view())
]