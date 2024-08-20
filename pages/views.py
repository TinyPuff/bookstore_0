from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import get_user_model
from books.models import Book

# Create your views here.

User = get_user_model()

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class BooksPageView(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'

class BookDetailsPageView(DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'
