# Generated by Django 4.1.4 on 2023-01-05 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='review',
            field=models.CharField(max_length=1000, verbose_name='Отзыв'),
        ),
    ]
