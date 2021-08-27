from django.core.management.base import BaseCommand
from products.utils import crawl_product
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Get data from the specified category or all of them'

    def add_arguments(self, parser):
        parser.add_argument(
            'category',
            type=str,
            help=
            'name of the category (all, phones, laptops, tablets, tvs, printers)'
        )
        parser.add_argument(
            'page_number_limit',
            type=int,
            nargs='?',
            default=1,
            help='gather data from page 1 upto this page number, defaults to 1'
        )

    def handle(self, *args, **options):
        category = options['category']
        page_number_limit = options['page_number_limit']

        category_urls = {
            'phones':
            'https://www.mobit.ir/search/digital-devices/mobile/mobilephone?sort=-view&page={page_number}',
            'laptops':
            'https://www.mobit.ir/search/digital-devices/laptop/laptop-ultrabook?sort=-view&page={page_number}',
            'tablets':
            'https://www.mobit.ir/search/digital-devices/tablets-readers/tablet?sort=-view&page={page_number}',
            'tvs':
            'https://www.mobit.ir/search/digital-devices/audiovisual-equipment/television?sort=-view&page={page_number}',
            'printers':
            'https://www.mobit.ir/search/digital-devices/computer-equipments/computer-devices/printer?sort=-view&page={page_number}'
        }

        def get_or_create_data(category, url):
            product_data = crawl_product(url, page_number_limit)

            category, created = Category.objects.get_or_create(name=category)
            for product in product_data:
                Product.objects.get_or_create(**product, category=category)

        if category == 'all':
            for category, url in category_urls.items():
                get_or_create_data(category, url)
        else:
            url = category_urls[category]
            get_or_create_data(category, url)
