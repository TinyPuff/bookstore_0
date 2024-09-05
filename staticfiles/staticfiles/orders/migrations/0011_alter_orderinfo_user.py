# Generated by Django 5.0.7 on 2024-09-01 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_emailaddress_unique_primary_email'),
        ('orders', '0010_alter_orderinfo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.emailaddress'),
        ),
    ]
