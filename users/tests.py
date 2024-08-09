from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy, resolve
from .forms import CustomUserCreationForm
from .views import SignUpPageView

# Create your tests here.


class CustomUserTests(TestCase):
    
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='testsuperuser',
            email='testsuperuser@email.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testsuperuser')
        self.assertEqual(user.email, 'testsuperuser@email.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class SignUpPageTests(TestCase):

    def setUp(self):
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    def test_signup_page_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hooo')
    
    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, SignUpPageView.as_view().__name__)


class LogInPageTests(TestCase):

    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)

    def test_login_page_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/login.html')
        self.assertContains(self.response, 'Log In')
        self.assertNotContains(self.response, 'Hooo')
    