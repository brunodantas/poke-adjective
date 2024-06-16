from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:letter>", view=views.poke_adj, name="poke_adj"),
]
