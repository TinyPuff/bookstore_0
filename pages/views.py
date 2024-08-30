from typing import Any
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth import get_user_model
from books.models import Book
from django.db.models import Q
from orders.models import Cart
from django.contrib import messages
from allauth.account.models import EmailAddress
from django.http import HttpResponseRedirect

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
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        # Call the parent get method to retrieve the product
        response = super().get(request, *args, **kwargs)
        product = self.get_object()

        # Store the selected product ID and price in the session
        request.session['selected_product_id'] = str(product.id)
        request.session['selected_product_price'] = int(product.price)
        request.session['selected_product_stock'] = int(product.stock)

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
    
class CartPageView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = "shoppingcart.html"
    context_object_name = "cartitems"
    login_url = 'account_login'

    def get_queryset(self):
        email = EmailAddress.objects.get(user=self.request.user)
        return Cart.objects.filter(user=email)
    
class AddToCartView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def post(self, request, product_id):
        product = get_object_or_404(Book, id=product_id)
        email = EmailAddress.objects.get(user=self.request.user)
        # expected_quantity = int(request.session.get('selected_product_stock'))

        # I think this part is completely unnecessary (the whole session thing)...
        # if expected_quantity == product_quantity:
        # check if that product is in stock
        try:
            # Get the product quantity from the form POST data 
            product_quantity = int(request.POST.get('product_quantity'))
            if product.stock >= 1 and product_quantity > 0:
                cart_item, created = Cart.objects.get_or_create(user=email, product=product)
            else:
                return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
            
            msg = f"Added {product_quantity} x {product.title} to your cart."
            # if the item is already in the cart and the requested quantity doesn't exceed the amount in stock, increase the quantity.
            if (not created) and ((cart_item.quantity + product_quantity ) <= product.stock):
                cart_item.quantity += product_quantity
                messages.success(request, msg)
            # if the item isn't in the cart and the requested quantity doesn't exceed the amount in stock, add to cart.
            elif created and (product_quantity <= product.stock):
                cart_item.quantity = product_quantity
                messages.success(request, msg)
            # if the requested quantity exceeds the amount in stock, redirect to book page.
            elif (not created) and (((cart_item.quantity + product_quantity ) > product.stock) or (product_quantity > product.stock)) :
                if ((product_quantity - product.stock) <= 0) and (cart_item.quantity != product.stock):
                    cart_item.quantity = product.stock
                    cart_item.save()
                    messages.success(request, f"Added {product.stock} x {product.title} to your cart.")
                    return redirect('cart')
                else:
                    messages.error(request, "The requested quantity exceeds the amount in stock.")
                    return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

            cart_item.save()


            return redirect('cart')
        except:
            messages.error(request, "Invalid input.")
            return HttpResponseRedirect(self.request.META['HTTP_REFERER'])

class DeleteFromCartView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def post(self, request, product_id):
        cart_item = get_object_or_404(Cart, id=product_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        elif cart_item.quantity <= 1:
            cart_item.delete()
        
        messages.success(request, f"Removed 1 x {cart_item.product.title} from your cart.")
        return redirect('cart')
        

class EditCartView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def post(self, request, product_id):
        try:
            cart_item = get_object_or_404(Cart, id=product_id)
            product_quantity = int(self.request.POST.get('product_quantity'))

            if product_quantity == 0:
                cart_item.delete()
                messages.success(request, f"{cart_item.product.title} has been removed from cart.")
                return redirect('cart')
            elif product_quantity == cart_item.quantity:
                return redirect('cart')
            elif product_quantity != cart_item.quantity:
                if product_quantity <= cart_item.product.stock:
                    cart_item.quantity = product_quantity
                    messages.success(request, f"You now have {cart_item.quantity} x {cart_item.product.title} in your cart.")
                    cart_item.save()
                    return redirect('cart')
                elif product_quantity > cart_item.product.stock:
                    messages.error(request, "The requested quantity exceeds the amount in stock.")
                    return redirect('cart')
        except:
            messages.error(request, "Invalid input.")
            return redirect('cart')
        

# To-Do: Let the users change the quantity from the cart and also the book_details page.
# Add a Check-Out button to the cart and fix the callback