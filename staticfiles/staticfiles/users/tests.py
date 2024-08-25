from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy, resolve
from .forms import CustomUserCreationForm

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
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123'
        )
        self.url = reverse('account_signup')
        self.response = self.client.get(self.url)

    def test_signup_page_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hooo')
    
    def test_signup_form(self):
        form = self.response.context.get('form')
        # self.assertIsInstance(form, CustomUserCreationForm) # fails when using django-allauth
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        self.assertEqual(self.User.objects.all().count(), 1)
        self.assertEqual(self.User.objects.all()[0].username, self.user.username)
        self.assertEqual(self.User.objects.all()[0].email, self.user.email)


class LogInPageTests(TestCase):

    def setUp(self):
        url = reverse('account_login')
        self.response = self.client.get(url)

    def test_login_page_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/login.html')
        self.assertContains(self.response, 'Log In')
        self.assertNotContains(self.response, 'Hooo')
    