from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    products_count = models.DecimalField(verbose_name='Количество товара', max_digits=8, decimal_places=2, default=0)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование')
    specifications = models.TextField(
        verbose_name='Характеристики',
        blank=True
    )
    price_now = models.DecimalField(
        verbose_name='Текущая цена',
        max_digits=8,
        decimal_places=2,
        default=0,
        null=True,
    )
    price_old = models.DecimalField(
        verbose_name='Предыдущая цена',
        max_digits=8,
        decimal_places=2,
        default=0
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество на складе',
        default=0
    )
    image1 = models.URLField(
        max_length=256,
        null=True,
    )
    image2 = models.URLField(
        max_length=256,
        null=True,
    )
    image3 = models.URLField(
        max_length=256,
        null=True,
    )
    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL"
    )
    short_description = models.CharField(
        verbose_name='Краткое описание',
        max_length=1000,
        blank=True,
        null = True,
    )
    description = models.TextField(
        verbose_name='Полное описание',
        blank=True,
        null=True,
    )
    colors = models.CharField(
        verbose_name='Цвета',
        max_length=100,
        blank=True
    )
    discount = models.DecimalField(
        verbose_name='Скидка',
        blank=True,
        null=True,
        max_digits=8,
        decimal_places=0,
    )
    brand = models.CharField(
        verbose_name='Бренд',
        max_length=255,
        blank=True,
        null=True,
    )




    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'


