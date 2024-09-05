from django.db import models
from django.contrib.auth import get_user_model
from books.models import Book
from django.core.exceptions import ValidationError
from allauth.account.models import EmailAddress
from django.urls import reverse

# Create your models here.

class OrderInfo(models.Model):
    gateway_id = models.PositiveIntegerField()
    user = models.ForeignKey(EmailAddress, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    tracking_code = models.PositiveBigIntegerField()
    post_tracking_code = models.PositiveBigIntegerField(default=0) # this one is different from the tracking code seen in the bank gateway. it's for the postal office.
    created_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=200, default="")
    total_products = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Order Info'

    def __str__(self):
        return f"{self.user} ({self.gateway_id})"
    
    def get_absolute_url(self):
        return reverse('order', args=[str(self.id)])

class OrderedProductsInfo(models.Model):
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

# add purchased products page

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