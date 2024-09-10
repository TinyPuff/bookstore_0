from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.models import EmailAddress

# Create your models here.


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    # make it so that the user can change their email later on
    user = models.OneToOneField(EmailAddress, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    zipcode = models.PositiveIntegerField(blank=True, null=True)
