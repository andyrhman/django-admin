from django.contrib import admin
from django.urls import path

from .views import AuthenticatedUser, users, register, login

urlpatterns = [
    path("users", users),
    path("register", register),
    path("login", login),
    path("user", AuthenticatedUser.as_view())
]