from django.urls import path

from . import views

urlpatterns = [
    path("<str:blogname>", views.isitabot, name="isitabot"),
]