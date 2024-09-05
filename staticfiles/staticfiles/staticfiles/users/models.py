from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from books.models import Book
from allauth.account.models import EmailAddress

# Create your models here.


class CustomUser(AbstractUser):
    pass

