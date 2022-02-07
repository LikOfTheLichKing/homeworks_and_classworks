from django.contrib import admin
from .models import Author, Book, BookInstance, Genre

admin.site.register([Author, Book, BookInstance, Genre])
