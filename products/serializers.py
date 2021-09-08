from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category', 'image', 'created_time',
            'updated_time'
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:category_detail', lookup_url_kwarg='category_id')
    products = serializers.HyperlinkedRelatedField(
        view_name='products:product_detail',
        lookup_url_kwarg='product_id',
        many=True,
        read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'products']
