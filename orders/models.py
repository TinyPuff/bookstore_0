from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(EmailAddress, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def clean(self):
        if self.quantity > self.product.stock:
            if self.product.stock == 1:
                msg = f"There is only {self.product.stock} in stock."
            elif self.product.stock > 1:
                msg = f"There are only {self.product.stock} in stock."
            elif self.product.stock == 0:
                msg= "There is none in stock."
            raise ValidationError({'quantity': msg})
    
    # use the session framework to store the cart items

    def __str__(self):
        return f"{self.quantity} x {self.product}"