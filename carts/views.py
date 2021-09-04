from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F

from .models import Cart, Entry
from products.models import Product


class CartDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cart
    template_name = 'carts/cart_detail.html'
    context_object_name = 'cart'
    pk_url_kwarg = 'cart_id'

    def get_queryset(self, *args, **kwargs):
        """ only the current user can see its own cart """
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    entry, created = Entry.objects.get_or_create(product=product)
    entry.quantity = F('quantity') + 1
    entry.save()
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.entries.add(entry)
    cart.save()
    return redirect('carts:cart_detail', cart_id=cart.id)
