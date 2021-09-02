from django.views import generic

from .models import Category, Product


class CategoryListView(generic.ListView):
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'products/category_list.html'


class ProductListView(generic.ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'products/product_list.html'


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'
