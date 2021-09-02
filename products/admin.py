import humanize

from django.contrib import admin

from .models import Product, Category


@admin.action(description='Make selected as not available')
def make_not_available(modeladmin, request, queryset):
    queryset.update(available=False)


class ProductInline(admin.TabularInline):
    model = Product
    extras = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_price', 'created_time',
                    'updated_time')
    list_filter = ('category', )
    search_fields = ('name', )
    date_hierarchy = 'created_time'
    actions = (make_not_available, )

    @admin.display(description='price')
    def get_price(self, obj):
        return humanize.intword(obj.price)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time', 'updated_time')
    inlines = (ProductInline, )
