from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
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

class BooksPageView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    login_url = 'account_login'

class BookDetailsPageView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'
    login_url = 'account_url'
    permission_required = 'books.special_status'
    permission_denied_message = "You don't have the permission to view this page."
