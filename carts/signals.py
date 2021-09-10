from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Cart


@receiver(m2m_changed, sender=Cart.entries.through)
def update_cart_total(sender, instance, action, **kwargs):
    prices = [entry.price for entry in instance.entries.all()]
    instance.total_price = sum(prices)
    instance.save()
