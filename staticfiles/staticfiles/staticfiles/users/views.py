from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views import generic
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

# Create your views here.

User = get_user_model()


class SignUpPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')