from django.db import models


class Product(models.Model):
    name = models.SlugField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return f'name:{self.name} | price: {self.price}'


# class Category(models.Model):
#     pass
