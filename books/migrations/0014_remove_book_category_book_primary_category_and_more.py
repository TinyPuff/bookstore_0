# Generated by Django 5.0.7 on 2024-09-07 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_bookcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
        migrations.AddField(
            model_name='book',
            name='primary_category',
            field=models.ManyToManyField(related_name='books', to='books.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='secondary_category',
            field=models.ManyToManyField(related_name='sbooks', to='books.category'),
        ),
    ]
