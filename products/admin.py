from django.contrib import admin

from .models import Product, Category


@admin.action(description='Make selected as not available')
def make_not_available(modeladmin, request, queryset):
    queryset.update(available=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    list_filter = ('category', )
    search_fields = ('name', )
    date_hierarchy = 'created_at'
    actions = (make_not_available, )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
