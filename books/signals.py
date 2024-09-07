from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Book, Category, BookCategory

# make it so that if the categories of a book are changed, the changes apply to BookCategory
@receiver(m2m_changed, sender=Book.primary_category.through)
def create_book_category(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for category_id in pk_set:
            BookCategory.objects.get_or_create(book=instance, category_id=category_id)