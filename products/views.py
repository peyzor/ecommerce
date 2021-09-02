from django.views import generic

from .models import Category


class CategoryListView(generic.ListView):
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'products/category_list.html'
