from django.db import models
from django.urls import reverse
import uuid

# Create your models here.


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    # cover = models.ImageField(upload_to="uploads/")
    title = models.CharField(max_length=350)
    author = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    details = models.TextField(max_length=1000, default="")

    def __str__(self):
        return (f"{self.author} - {self.title}")
    
    def get_absolute_url(self):
        return reverse("book_details", args=[str(self.pk)])