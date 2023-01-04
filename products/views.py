from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from products.forms import ReviewsForm
from products.models import Product, ProductCategory, Basket, User, Reviews
from products.scraping import scraping


class ProductsListView(ListView):
    model = Product, User
    template_name = 'products/store.html'
    title = 'Store - Каталог'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        try:
            context['baskets'] = Basket.objects.filter(user=self.request.user)
        except:
            context['baskets'] = None
        context['categories'] = ProductCategory.objects.annotate(items_count=Count('product'))
        context['brands'] = Product.objects.values('brand').distinct().order_by('brand').annotate(
            items_count=Count('brand'))
        context['random'] = Product.objects.order_by("?")
        context['max_price'] = int(Product.objects.all().order_by('price_old').last().price_old)
        context['min_price'] = int(Product.objects.all().order_by('-price_old').last().price_old)
        if 'Category' in self.request.GET and 'Brand' in self.request.GET:
            brand_filtr = Product.objects.filter(category_id__in=self.request.GET.getlist("Category"))
            context['brands'] = brand_filtr.values('brand').distinct().order_by('brand').annotate(
                items_count=Count('brand'))
            category_filtr = ProductCategory.objects.filter(product__brand__in=self.request.GET.getlist("Brand"))
            context['categories'] = category_filtr.annotate(items_count=Count('product'))
        elif 'Category' in self.request.GET:
            brand_filtr = Product.objects.filter(category_id__in=self.request.GET.getlist("Category"))
            context['brands'] = brand_filtr.values('brand').distinct().order_by('brand').annotate(
                items_count=Count('brand'))
        elif 'Brand' in self.request.GET:
            category_filtr = ProductCategory.objects.filter(product__brand__in=self.request.GET.getlist("Brand"))
            context['categories'] = category_filtr.annotate(items_count=Count('product'))
        query = f"{'&Search='+self.request.GET.get('Search') if self.request.GET.get('Search') else ''}" \
                f"{'&Category='+self.request.GET.get('Category') if self.request.GET.get('Category') else ''}" \
                f"{'&Brand='+self.request.GET.get('Brand') if self.request.GET.get('Brand') else ''}"
        context['query'] = query



        return context

    def get_queryset(self):
        queryset = Product.objects.order_by("?")
        if 'Search' in self.request.GET:
            queryset = Product.objects.filter(name__iregex=self.request.GET.get("Search"))
        elif 'Category' in self.request.GET and 'Brand' in self.request.GET:
            queryset = Product.objects.filter(
                Q(category_id__in=self.request.GET.getlist("Category")), Q(brand__in=self.request.GET.getlist("Brand")))
        elif 'Category' in self.request.GET or 'Brand' in self.request.GET:
            queryset = Product.objects.filter(
                Q(category_id__in=self.request.GET.getlist("Category")) | Q(brand__in=self.request.GET.getlist("Brand")))


        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    title = 'Store - Каталог'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['form'] = ReviewsForm()
        context['colors'] = self.get_object().colors.split(",")
        try:
            context['baskets'] = Basket.objects.filter(user=self.request.user)
        except:
            context['baskets'] = None
        context['reviews'] = Reviews.objects.filter(product__id=self.object.id)
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
    if 'Color' in request.GET and 'Quantity' in request.GET:
        if baskets.exists() and baskets.first().color == request.GET['Color']:
            basket = baskets.first()
            basket.quantity += int(request.GET['Quantity'])
            basket.save()
        else:
            Basket.objects.create(user=request.user, product=product,
                                  quantity=request.GET['Quantity'], color=request.GET['Color'])
    elif 'Quantity' in request.GET:
        if baskets.exists():
            basket = baskets.first()
            basket.quantity += int(request.GET['Quantity'])
            basket.save()
        else:
            Basket.objects.create(user=request.user, product=product,
                                  quantity=request.GET['Quantity'])

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove_all(request, basket_id):
    test = Basket.objects.all().filter(user=request.user)
    test.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def review_add(request, product_id):
    product = Product.objects.get(id=product_id)
    Reviews.objects.create(user=request.user, product=product,
                           review=request.POST['review'], stars=request.POST['stars'])
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


