from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth import get_user_model

# Create your models here.


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    cover = models.ImageField(upload_to="covers/", blank=True)
    title = models.CharField(max_length=350)
    author = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    details = models.TextField(max_length=1000, default="")

    class Meta:
        permissions = [
            ('special_status', 'Can read all books')
        ]

    def __str__(self):
        return (f"{self.author} - {self.title}")
    
    def get_absolute_url(self):
        return reverse("book_details", args=[str(self.pk)])

class Review(models.Model):

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    review = models.CharField(max_length=250)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.review[:50]