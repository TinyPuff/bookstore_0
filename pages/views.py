from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'
