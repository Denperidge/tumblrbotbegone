from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("redirect", views.redirect_callback, name="redirect"),
    path("logout", views.logout, name="logout")
]