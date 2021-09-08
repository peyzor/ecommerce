from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product, Category


class ProductHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    view_name = 'products:product_detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {'category': obj.category, 'product_id': obj.pk}
        return reverse(view_name,
                       kwargs=url_kwargs,
                       request=request,
                       format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'category': view_kwargs['category'],
            'pk': view_kwargs['product_id']
        }
        return self.get_queryset().get(**lookup_kwargs)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = ProductHyperlinkedRelatedField(read_only=True)
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
    products = ProductHyperlinkedRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'products']
