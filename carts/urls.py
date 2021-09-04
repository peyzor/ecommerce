from django.urls import path

from . import views

urlpatterns = [
    path('cart-detail/<int:cart_id>/',
         views.CartDetailView.as_view(),
         name='cart_detail'),
]