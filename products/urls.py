from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.RootView.as_view(), name='root'),
    path('categories/', views.CategoryListView.as_view(),
         name='category_list'),
    path('categories/<int:category_id>/',
         views.CategoryDetailView.as_view(),
         name='category_detail'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('<str:category>/products/<int:product_id>/',
         views.ProductDetailView.as_view(),
         name='product_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
