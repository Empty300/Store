from django.views.generic import ListView

from products.models import Product, Basket


class IndexView(ListView):
    template_name = 'main/index.html'
    model = Product
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['sale_prod'] = Product.objects.exclude(discount=None).order_by('-discount')[0:7]
        try:
            context['baskets'] = Basket.objects.filter(user=self.request.user)
        except:
            context['baskets'] = None
        context['random'] = Product.objects.order_by("?")[0:7]
        return context
