from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('category-list/',
         views.CategoryListView.as_view(),
         name='category_list'),
    path('<str:category>/product-list/',
         views.ProductListView.as_view(),
         name='product_list'),
    path('product-detail/<int:product_id>/',
         views.ProductDetailView.as_view(),
         name='product_detail'),
    path('api/', views.RootAPIView.as_view(), name='root_api'),
    path('api/products/',
         views.ProductListAPIView.as_view(),
         name='product_list_api'),
    path('api/products/<int:pk>/',
         views.ProductDetailAPIView.as_view(),
         name='product_detail_api'),
    path('api/categories/',
         views.CategoryListAPIView.as_view(),
         name='category_list_api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
