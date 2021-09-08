from rest_framework import serializers

from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category', 'image', 'created_time',
            'updated_time'
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:category_detail_api')
    product_set = serializers.HyperlinkedRelatedField(
        view_name='products:product_detail_api',
        lookup_field='pk',
        many=True,
        read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'product_set']
