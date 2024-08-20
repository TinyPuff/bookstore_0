from django.urls import path
from .views import HomePageView, AboutPageView, BooksPageView, BookDetailsPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('books/', BooksPageView.as_view(), name='books'),
    path('book/<uuid:pk>/', BookDetailsPageView.as_view(), name='book_details'),
]