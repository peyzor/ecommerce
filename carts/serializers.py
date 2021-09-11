from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Cart, Entry
from products.models import Product


class ProductHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    view_name = 'products:product_detail'

    def get_url(self, obj, view_name, request, format):
        product = Product.objects.get(pk=obj.pk)
        url_kwargs = {'category': product.category, 'product_id': obj.pk}
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


class CartSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='carts:cart_detail',
                                               lookup_url_kwarg='cart_id')
    entries = serializers.HyperlinkedRelatedField(
        view_name='carts:entry_detail',
        lookup_url_kwarg='entry_id',
        many=True,
        read_only=True)

    class Meta:
        model = Cart
        fields = [
            'url', 'entries', 'total_price', 'created_time', 'updated_time',
            'available'
        ]


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='carts:entry_detail',
                                               lookup_url_kwarg='entry_id')
    product = ProductHyperlinkedRelatedField(read_only=True)

    class Meta:
        model = Entry
        fields = ['url', 'product', 'quantity', 'price']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        add_to_cart_link = reverse('carts:add_to_cart',
                                   kwargs={'product_id': instance.product.id},
                                   request=self.context.get('request'))
        output = {**data, 'add_to_cart': add_to_cart_link}
        return output
