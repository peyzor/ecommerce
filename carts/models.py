from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE)
    entries = models.ManyToManyField(
        'Entry',
        verbose_name=_('entries'),
    )
    total_price = models.PositiveIntegerField(
        _('total price'),
        blank=True,
        null=True,
    )
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    available = models.BooleanField(_('available'), default=True)

    class Meta:
        db_table = 'cart'
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return f'{self.user}, {self.total_price}'

    def get_absolute_url(self):
        return reverse('carts:cart_detail', kwargs={'pk': self.pk})


class Entry(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name=_('entry'),
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_('quantity'))
    price = models.PositiveIntegerField(_('price'), blank=True, null=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'entry'
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __str__(self):
        return f'{self.product}, {self.quantity}'
