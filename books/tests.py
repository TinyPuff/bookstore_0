from django.test import TestCase
from django.urls import reverse
from .models import Book, Review
from django.contrib.auth import get_user_model

# Create your tests here.


class BookTests(TestCase):
    
    def setUp(self):
        self.book = Book.objects.create(
            title='Book Title',
            author='Book Author',
            price=10,
            details='Book Details',
        )
        self.user = get_user_model().objects.create(
            username='testuser',
            email='testuser@email.com',
            password='testpass123',
        )
        self.review = Review.objects.create(
            book=self.book,
            author=self.user,
            review='text',
        )
    
    def test_books_list_view(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book Title')
        self.assertTemplateUsed(response, 'books.html')
    
    def test_books_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('books/123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Book Details')
        self.assertContains(response, 'text')
        self.assertTemplateUsed(response, 'book_details.html')