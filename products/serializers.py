from rest_framework import serializers

from .models import Product, Category


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:product_detail',
        lookup_url_kwarg='product_id',
        read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'url', 'id', 'name', 'price', 'category', 'image', 'created_time',
            'updated_time'
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:category_detail',
        lookup_url_kwarg='category_id',
        read_only=True)
    products = serializers.HyperlinkedRelatedField(
        view_name='products:product_detail',
        lookup_url_kwarg='product_id',
        many=True,
        read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'products']
