from django.db import models

from users.models import User


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
        max_length=10000,
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
    def sum(self):
        all_stars=list()
        all_reviews = Reviews.objects.all().filter(product=self.id)
        if all_reviews:
            for star in all_reviews:
                all_stars.append(star.stars)
            return sum(all_stars)/len(all_reviews)
        else:
            return 'Оценок недостаточно'


    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()
    color = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return f'Продукт: {self.user.username} | Категория: {self.product.name}'

    def sum(self):
        if self.product.price_now:
            return self.product.price_now * self.quantity
        else:
            return self.product.price_old * self.quantity


class Reviews(models.Model):
    review = models.CharField(
        verbose_name='Отзыв',
        max_length=1000,
    )
    stars = models.PositiveSmallIntegerField(verbose_name='Оценка')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Продукт')


