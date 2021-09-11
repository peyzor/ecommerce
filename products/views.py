from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from products.serializers import ProductSerializer, CategorySerializer
from .models import Category, Product


class RootView(APIView):
    def get(self, request, format=None):
        return Response({
            'categories':
            reverse('products:category_list', request=request, format=format),
            'products':
            reverse('products:product_list', request=request, format=format),
            'entries':
            reverse('carts:entry_list', request=request, format=format),
        })


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'category_id'
