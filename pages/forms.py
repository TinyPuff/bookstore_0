from books.models import Book, Category
from django import forms


class SearchForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'primary_category',]
