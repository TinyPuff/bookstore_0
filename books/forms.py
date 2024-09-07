from django import forms
from .models import Book, Category
from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover', 'title', 'author', 'price', 'details', 'stock', 'primary_category', 'secondary_category',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # in a book instance, exclude the chosen primary categories from the secondary category options
        if self.instance and self.instance.pk:
            primary_category = self.instance.primary_category.all()
            self.fields['secondary_category'].queryset = Category.objects.exclude(id__in=primary_category)
    
    def clean_primary_category(self):
        primary_category = self.cleaned_data['primary_category']
        if primary_category.count() > 2:
            raise ValidationError("You can select up to 2 primary categories!")
        """for tag in primary_category:
            if tag in secondary"""
        return primary_category