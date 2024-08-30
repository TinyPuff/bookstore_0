from django.contrib import admin
from .models import Category, Book, Review

# Register your models here.


class ReviewInline(admin.TabularInline):
    model = Review


class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ("title", "author", "price", "stock")

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        BookInline
    ]




admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)