from django.urls import path

from . import views

app_name = 'carts'
urlpatterns = [
    path('entries/', views.EntryListView.as_view(), name='entry_list'),
    path('entries/<int:entry_id>/',
         views.EntryDetailView.as_view(),
         name='entry_detail'),
    path('<int:cart_id>/', views.CartDetailView.as_view(), name='cart_detail'),
    path('add-to-cart/products/<int:product_id>/',
         views.AddToCartView.as_view(),
         name='add_to_cart'),
]
