import humanize
from django.contrib import admin

from .models import Cart, Entry


@admin.action(description='Make selected as not available')
def make_not_available(modeladmin, request, queryset):
    queryset.update(available=False)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'get_price')

    @admin.display(description='price')
    def get_price(self, obj):
        return humanize.intword(obj.price)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'created_time', 'updated_time',
                    'available')
    actions = (make_not_available, )
