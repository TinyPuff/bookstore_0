# Generated by Django 5.0.7 on 2024-08-30 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_category_book_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
