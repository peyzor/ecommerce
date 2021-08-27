from django.core.management.base import BaseCommand, CommandError
from products.utils import crawl_product
from products.models import Product, Category


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('page_number_limit', type=int)
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        url = 'https://www.mobit.ir/search/digital-devices/mobile/mobilephone?sort=-view&page={page_number}'
        data = crawl_product(url, options['page_number_limit'])

        category, created = Category.objects.get_or_create(
            name=options['category'])
        for product in data:
            Product.objects.get_or_create(**product, category=category)
