from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('category-list/',
         views.CategoryListView.as_view(),
         name='category_list'),
    path('<str:category>/product-list/',
         views.ProductListView.as_view(),
         name='product-list'),
    path('product-detail/<int:product_id>',
         views.ProductDetailView.as_view(),
         name='product-detail'),
]
