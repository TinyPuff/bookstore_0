from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from books.models import Book
from allauth.account.models import EmailAddress

# Create your models here.


class CustomUser(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(EmailAddress, on_delete=models.CASCADE)
    owned_books = models.ManyToManyField(Book, related_name='owners')

    def __str__(self):
        return self.user.email