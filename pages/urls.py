from django.urls import path
from .views import (HomePageView, AboutPageView, BooksPageView, BookDetailsPageView, SearchResultsPageView, CartPageView,
AddToCartView, DeleteFromCartView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('books/', BooksPageView.as_view(), name='books'),
    path('book/<uuid:pk>/', BookDetailsPageView.as_view(), name='book_details'),
    path('search/', SearchResultsPageView.as_view(), name='search_results'),
    path('cart/', CartPageView.as_view(), name='cart'),
    path('addtocart/<uuid:product_id>/', AddToCartView.as_view(), name='addtocart'),
    path('deletefromcart/<int:product_id>/', DeleteFromCartView.as_view(), name='deletefromcart')
]