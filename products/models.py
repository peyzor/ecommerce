from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    price = models.PositiveIntegerField(_('price'))
    category = models.ForeignKey('Category',
                                 verbose_name=_('category'),
                                 on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    available = models.BooleanField(_('available'), default=True)

    class Meta:
        db_table = 'product'
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def get_absolute_url(self):
        return reverse('products:product_detail',
                       kwargs={'product_id': self.id})

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def get_absolute_url(self):
        return reverse('products:product_list', kwargs={'category': self.name})

    def __str__(self):
        return self.name
