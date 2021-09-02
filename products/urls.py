from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('category-list',
         views.CategoryListView.as_view(),
         name='category_list'),
]
