from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView

from common.views import CommonMixin
from products.forms import ReviewsForm
from products.models import Basket, Product, ProductCategory, Reviews, User
from products.scraping import scraping


class CategoriesListView(CommonMixin, ListView):
    model = ProductCategory
    template_name = 'products/categories.html'
    title = 'Store - Категории'

    def get_queryset(self):
        queryset = ProductCategory.objects.all().order_by('id')
        return queryset


class ProductsListView(CommonMixin, ListView):
    model = Product, User
    template_name = 'products/store.html'
    title = 'Store - Каталог'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['category'] = ProductCategory.objects.get(id=self.kwargs['category_id'])
        context['old_order'] = self.request.GET['order'] if 'order' in self.request.GET else 'discount'
        context['old_min_price'] = self.request.GET['min_price'] if 'min_price' in self.request.GET else None
        context['old_max_price'] = self.request.GET['max_price'] if 'max_price' in self.request.GET else None
        if 'Brand' not in self.request.GET:
            context['max_price'] = int(Product.objects.filter(category_id=self.kwargs['category_id'])
                                       .order_by('price_now').last().price_now)
            context['min_price'] = int(Product.objects.filter(category_id=self.kwargs['category_id'])
                                       .order_by('-price_now').last().price_now)
        else:
            context['max_price'] = int(Product.objects.filter(category_id=self.kwargs['category_id'],
                                                              brand=self.request.GET.get('Brand'))
                                       .order_by('price_now').last().price_now)
            context['min_price'] = int(Product.objects.filter(category_id=self.kwargs['category_id'],
                                                              brand=self.request.GET.get('Brand'))
                                       .order_by('-price_now').last().price_now)
        brand_filtr = Product.objects.filter(category_id=self.kwargs['category_id']).values(
            'brand').distinct().annotate(
            items_count=Count('brand'))
        context['brands'] = brand_filtr.order_by('-items_count')
        query = f"{'&Search=' + self.request.GET.get('Search') if self.request.GET.get('Search') else ''}" \
                f"{'&Brand=' + self.request.GET.get('Brand') if self.request.GET.get('Brand') else ''}" \
                f"{'&min_price=' + self.request.GET.get('min_price') if self.request.GET.get('min_price') else ''}" \
                f"{'&max_price=' + self.request.GET.get('max_price') if self.request.GET.get('max_price') else ''}" \
                f"{'&order=' + self.request.GET.get('order') if self.request.GET.get('order') else ''}"
        context['query'] = query

        return context

    def get_queryset(self):
        if 'Brand' in self.request.GET and 'max_price' in self.request.GET:
            queryset = Product.objects.filter(category_id=self.kwargs['category_id'],
                                              brand__in=self.request.GET.getlist("Brand"),
                                              price_now__gte=self.request.GET.get("min_price")[:-1] if
                                              isinstance(self.request.GET.get("min_price")[:-1], str) else 0,
                                              price_now__lte=self.request.GET.get("max_price")[:-1] if
                                              isinstance(self.request.GET.get("min_price")[:-1], str) else 1000000
                                              ).order_by((F('discount').desc(nulls_last=True) if
                                                          'discount' in self.request.GET['order']
                                                          else self.request.GET
                                                          ['order']) if 'order' in self.request.GET else 'name')
        elif 'Brand' not in self.request.GET and 'max_price' not in self.request.GET:
            queryset = Product.objects.all().filter(category_id=self.kwargs['category_id']) \
                .order_by((F('discount').desc(nulls_last=True) if 'discount' in self
                           .request.GET['order'] else self.request.GET['order']) if
                          'order' in self.request.GET else 'name')
        else:
            queryset = Product.objects.all().filter(category_id=self.kwargs['category_id'],
                                                    price_now__gte=self.request.GET.get("min_price")[:-1] if
                                                    isinstance(self.request.GET.get("min_price")[:-1], str) else 0,
                                                    price_now__lte=self.request.GET.get("max_price")[:-1] if
                                                    isinstance(self.request.GET.get("min_price")[:-1],
                                                               str) else 1000000) \
                .order_by((F('discount').desc(nulls_last=True) if 'discount' in self
                           .request.GET['order'] else self.request.GET['order']) if
                          'order' in self.request.GET else 'name')

        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['form'] = ReviewsForm()
        context['colors'] = self.get_object().colors.split(",")
        context['reviews'] = Reviews.objects.filter(product__id=self.object.id)
        context['specifications'] = self.get_object().specifications.split('\n')
        context['categories'] = ProductCategory.objects.all()
        context['title'] = self.object.name
        return context


def scrap(request):
    if request.method == 'POST' and request.user.is_staff:
        scraping()

    return render(request, 'products/fill-products.html', {'message': None})


class SearchListView(CommonMixin, ListView):
    model = Product
    template_name = 'products/search.html'
    title = 'Store - Поиск'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView, self).get_context_data()
        query = f"{'&Search=' + self.request.GET.get('Search') if self.request.GET.get('Search') else ''}"
        context['query'] = query
        context['search_name'] = self.request.GET['Search']
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(name__iregex=self.request.GET.get("Search"))
        return queryset



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
    else:
        Basket.objects.create(user=request.user, product=product,
                              quantity=1)

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


@login_required
def review_del(request, review_id):
    review = Reviews.objects.get(id=review_id)
    if request.user == review.user:
        review.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
