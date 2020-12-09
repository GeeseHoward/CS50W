from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.get_entry, name="get_entry"),
    path("search", views.search, name="search"),
    path("add", views.add_entry, name="add_entry"),
    path("edit/<str:entry_title>", views.edit_entry, name="edit_entry"),
    path("random", views.random_entry, name="random_entry")
]
