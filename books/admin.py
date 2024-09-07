from django.contrib import admin
from .models import Category, Book, Review, BookCategory
from .forms import BookForm

# Register your models here.


class ReviewInline(admin.TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    form = BookForm
    inlines = [
        ReviewInline,
    ]
    list_display = ("title", "author", "price", "stock")

class BookCategoryInline(admin.TabularInline):
    model = BookCategory
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        BookCategoryInline
    ]




admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)