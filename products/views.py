from django.views import generic

from .models import Category, Product


class CategoryListView(generic.ListView):
    queryset = Category.objects.all()
    template_name = 'products/category_list.html'
    context_object_name = 'categories'


class ProductListView(generic.ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category__name=self.kwargs['category'])


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
