from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.RootView.as_view(), name='root'),
    path('categories/', views.CategoryListView.as_view(),
         name='category_list'),
    path('categories/<int:pk>/',
         views.CategoryDetailView.as_view(),
         name='category_detail'),
    path('<str:category>/products/',
         views.ProductListView.as_view(),
         name='product_list'),
    path('products/<int:pk>/',
         views.ProductDetailView.as_view(),
         name='product_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
