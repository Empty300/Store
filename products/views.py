from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView


from products.models import Product, ProductCategory, Basket, User
from products.scraping import scraping


class ProductsListView(ListView):
    model = Product, User
    template_name = 'products/store.html'
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        context['categories'] = ProductCategory.objects.annotate(items_count=Count('product'))
        context['brands'] = Product.objects.values('brand').distinct().order_by('brand').annotate(
            items_count=Count('brand'))
        if 'Category' and 'Brand' in self.request.GET:
            test1 = Product.objects.values('brand').distinct().order_by('brand').annotate(
                items_count=Count('brand'))
            context['brands'] = test1.filter(category_id__in=self.request.GET.getlist("Category"))
            test = ProductCategory.objects.annotate(items_count=Count('product'))
            context['categories'] = test.filter(product__brand__in=self.request.GET.getlist("Brand"))
        elif 'Category' in self.request.GET:
             test = Product.objects.values('brand').distinct().order_by('brand').annotate(
                items_count=Count('brand'))
             context['brands'] = test.filter(category_id__in=self.request.GET.getlist("Category"))
        elif 'Brand' in self.request.GET:
            test = ProductCategory.objects.annotate(items_count=Count('product'))
            context['categories'] = test.filter(product__brand__in=self.request.GET.getlist("Brand"))
        else:
            context['brands'] = Product.objects.values('brand').distinct().order_by('brand').annotate(
                items_count=Count('brand'))
        context['random'] = Product.objects.order_by("?")

        return context

    def get_queryset(self):
        if 'Category' in self.request.GET and 'Brand' in self.request.GET:
            queryset = Product.objects.filter(
                Q(category_id__in=self.request.GET.getlist("Category")), Q(brand__in=self.request.GET.getlist("Brand")))
        elif 'Category' in self.request.GET or 'Brand' in self.request.GET:
            queryset = Product.objects.filter(
                Q(category_id__in=self.request.GET.getlist("Category"))| Q(brand__in=self.request.GET.getlist("Brand")))
        else:
            queryset = Product.objects.order_by("?")

        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['colors'] = self.get_object().colors.split(",")
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        context['specifications'] = self.get_object().specifications.split('\n')
        context['categories'] = ProductCategory.objects.all()
        return context


def scrap(request):
    if request.method == 'POST' and request.user.is_staff:
        scraping()

    return render(request, 'products/fill-products.html', {'message': None})


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


