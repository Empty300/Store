from django.contrib import admin
from products.models import ProductCategory, Product

admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_now', 'price_old', 'discount', 'brand')
    fields = ('name',  'quantity', 'category', 'slug', 'specifications', 'price_now', 'price_old', 'image1',
              'image2', 'image3', 'short_description', 'description', 'colors', 'brand')
    prepopulated_fields = {"slug": ("name",)}