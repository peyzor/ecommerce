# from django.contrib import admin

# from .models import Cart, Entry

# @admin.action(description='Make selected as not available')
# def make_not_available(modeladmin, request, queryset):
#     queryset.update(available=False)

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ('user', 'total_price', 'created_time', 'updated_time',
#                     'available')
#     actions = (make_not_available, )

# admin.site.register(Entry)