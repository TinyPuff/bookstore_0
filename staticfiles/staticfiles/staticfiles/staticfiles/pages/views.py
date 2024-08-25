from typing import Any
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth import get_user_model
from books.models import Book
from django.db.models import Q

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

class BookDetailsPageView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'
    login_url = 'account_url'

    def get(self, request, *args, **kwargs):
        # Call the parent get method to retrieve the product
        response = super().get(request, *args, **kwargs)
        product = self.get_object()

        # Store the selected product ID and price in the session
        request.session['selected_product_id'] = str(product.id)
        request.session['selected_product_price'] = int(product.price)

        return response
    
class SearchResultsPageView(ListView):
    model = Book
    template_name = "search_results.html"
    context_object_name = 'books'
    
    def get_queryset(self):
        query=self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )