from django.contrib import admin
from products.models import ProductCategory, Product, Basket, Reviews

admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_now', 'price_old', 'discount', 'brand')
    fields = ('name',  'quantity', 'category', 'slug', 'specifications', 'price_now', 'price_old', 'image1',
              'image2', 'image3', 'short_description', 'description', 'colors', 'brand')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_timestamp')
    fields = ('user', 'product', 'created_timestamp')
    readonly_fields = ['created_timestamp']



@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'stars', 'created_timestamp')
    fields = ('user', 'product', 'created_timestamp', 'stars', 'review')
    readonly_fields = ['created_timestamp']
