from django.urls import path

from . import views

app_name = 'carts'
urlpatterns = [
    path('cart-detail/<int:cart_id>/',
         views.CartDetailView.as_view(),
         name='cart_detail'),
    path('add-to-cart/<product_id>/',
         views.AddToCartView.as_view(),
         name='add_to_cart'),
]
