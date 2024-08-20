from django.test import TestCase
from django.urls import reverse
from .models import Book

# Create your tests here.


class BookTests(TestCase):
    
    def setUp(self):
        self.book = Book.objects.create(
            title='Book Title',
            author='Book Author',
            price=10,
            details='Book Details',
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
        self.assertTemplateUsed(response, 'book_details.html')