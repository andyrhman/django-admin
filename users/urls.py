from django.contrib import admin
from django.urls import path

from .views import users, register

urlpatterns = [
    path("users", users),
    path("register", register),
]