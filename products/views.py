from django.db.models import Count, Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from products.models import Product, ProductCategory
from products.scraping import scraping


class ProductsListView(ListView):
    model = Product
    template_name = 'products/store.html'
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.annotate(items_count=Count('product'))
        context['brands'] = Product.objects.values('brand').distinct().order_by('brand')

        return context


    # def get_queryset(self):
    #     queryset = Product.objects.filter(category_id__in=self.request.GET.getlist("Category"))
    #     return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['colors'] = self.get_object().colors.split(",")
        context['specifications'] = self.get_object().specifications.split('\n')
        context['categories'] = ProductCategory.objects.all()
        return context


class FilterListView(ListView):
    template_name = 'products/store.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FilterListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.annotate(items_count=Count('product'))
        context['brands'] = Product.objects.values('brand').distinct().order_by('brand')
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(category_id__in=self.request.GET.getlist("Category")) |
            Q(brand__in=self.request.GET.getlist("Brand")))
        return queryset





def scrap(request):
    if request.method == 'POST' and request.user.is_staff:
        scraping()

    return render(request, 'products/fill-products.html', {'message': None})



