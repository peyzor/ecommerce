from django.contrib import admin

from .models import Product


@admin.action(description='Make selected as not available')
def make_not_available(modeladmin, request, queryset):
    queryset.update(available=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    search_fields = ('name', )
    date_hierarchy = 'created_at'
    actions = (make_not_available, )
