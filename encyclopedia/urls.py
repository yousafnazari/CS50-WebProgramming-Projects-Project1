from unicodedata import name
from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.showEntry, name="showEntry"),
    path("search/", views.search, name="search"),
    path("newPage/", views.newPage, name="newPage"),
    path("saveNewEntry/", views.saveNewEntry, name="saveNewEntry"),
    path("editEntry/<str:name>", views.editEntry, name="editEntry"),
    path("saveEdit/<str:name>", views.saveEdit, name="saveEdit"),
    path("randomPage/", views.randomPage, name="randomPage")
]
