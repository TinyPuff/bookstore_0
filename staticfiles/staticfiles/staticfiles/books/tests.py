from django.test import TestCase
from django.urls import reverse
from .models import Book, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

# Create your tests here.


class BookTests(TestCase):
    
    def setUp(self):
        self.book = Book.objects.create(
            title='Book Title',
            author='Book Author',
            price='10.00',
            details='Book Details',
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass123',
        )
        self.special_permission = Permission.objects.get(codename='special_status')

        self.review = Review.objects.create(
            book=self.book,
            author=self.user,
            review='text',
        )
    
    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Book Title')
        self.assertEqual(f'{self.book.author}', 'Book Author')
        self.assertEqual(f'{self.book.price}', '10.00')

    def test_books_list_view_for_logged_in_users(self):
        self.client.login(email='testuser@email.com', password='testpass123')
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book Title')
        self.assertTemplateUsed(response, 'books.html')
    
    def test_books_list_view_for_logged_out_users(self):
        self.client.logout()
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/books/' % (reverse('account_login')))
        response = self.client.get('%s?next=/books/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')

    def test_books_detail_view(self):
        self.client.login(email='testuser@email.com', password='testpass123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('books/123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Book Details')
        self.assertContains(response, 'text')
        self.assertTemplateUsed(response, 'book_details.html')