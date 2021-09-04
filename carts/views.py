from django.views import generic

from .models import Cart


class CartDetailView(generic.DetailView):
    model = Cart
    template_name = 'carts/cart_detail.html'
    context_object_name = 'cart'
    pk_url_kwarg = 'cart_id'

    def get_queryset(self, *args, **kwargs):
        """ only the current user can see its own cart """
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)
