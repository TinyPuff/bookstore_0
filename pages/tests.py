from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomePageView

# Create your tests here.


class HomePageTests(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_page_status(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_home_page_url_name(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_home_page_template(self):
        self.assertTemplateUsed(self.response, 'home.html')
    
    def test_home_page_correct_html(self):
        self.assertContains(self.response, 'Home')
    
    def test_home_page_incorrect_html(self):
        self.assertNotContains(self.response, 'Hooo')

    def test_home_page_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)