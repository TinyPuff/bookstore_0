from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(18, message='You need to be 18 or older in order to sign up.')])
