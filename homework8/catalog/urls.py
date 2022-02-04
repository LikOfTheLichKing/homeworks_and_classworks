from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("books", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book"),
    path("authors", views.AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>", views.AuthorDetailView.as_view(), name="author"),
    path("authors/create", views.authorCreate, name="create author"),
]
