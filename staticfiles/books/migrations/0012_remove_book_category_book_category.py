# Generated by Django 5.0.7 on 2024-08-31 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_category_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(to='books.category'),
        ),
    ]
