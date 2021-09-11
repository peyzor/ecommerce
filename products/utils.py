import requests

from io import BytesIO
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from django.core import files

from products.models import Product


def crawl_product(url, page_number_limit):
    """
    gather data from the specified url page by page
    from page 1 upto `page_number_limit`

    Parameters
    ----------
    url : str
    page_number_limit : int

    Returns
    -------
    List[dict]
        data gathered from each product is added to the
        `data` list
    """
    data = []

    page_number = 1
    crawl = True
    while crawl:
        response = requests.get(url.format(page_number=page_number))
        crawl = response.ok

        soup = BeautifulSoup(response.text, features='html.parser')

        names = soup.select(
            '#inspire > div > div.lg\:tw-mt-6 > div:nth-child(2) > div > div > div > main > div.tw-grid.tw-grid-cols-1.tw-mt-4.tw-gap-y-3.sm\:tw-grid-cols-2.sm\:tw-gap-3.lg\:tw-gap-4.lg\:tw-grid-cols-3.xl\:tw-grid-cols-4 > a > section > div > div.tw-min-h-\[3\.5rem\].tw-whitespace-normal.tw-text-3xs.tw-grid.tw-place-items-center.lg\:tw-h-16 > h4'
        )

        prices = soup.select(
            '#inspire > div > div.lg\:tw-mt-6 > div:nth-child(2) > div > div > div > main > div.tw-grid.tw-grid-cols-1.tw-mt-4.tw-gap-y-3.sm\:tw-grid-cols-2.sm\:tw-gap-3.lg\:tw-gap-4.lg\:tw-grid-cols-3.xl\:tw-grid-cols-4 > a > section > div > div.tw-flex.tw-justify-between.tw-items-end > div.tw-flex.tw-flex-row.tw-justify-end.tw-items-end.tw-mt-2.lg\:tw-mt-0.lg\:tw-pt-0.tw-space-x-reverse.tw-space-x-2.lg\:tw-min-h-\[4\.5rem\] > div.tw-flex.tw-flex-col.tw-items-center.tw-justify-center > span.tw-flex.tw-items-center.tw-font-bold.tw-text-base.lg\:tw-order-2 > span'
        )

        discount_prices = soup.select(
            '#inspire > div > div.lg\:tw-mt-6 > div:nth-child(2) > div > div > div > main > div.tw-grid.tw-grid-cols-1.tw-mt-4.tw-gap-y-3.sm\:tw-grid-cols-2.sm\:tw-gap-3.lg\:tw-gap-4.lg\:tw-grid-cols-3.xl\:tw-grid-cols-4 > a > section > div > div.tw-flex.tw-justify-between.tw-items-end > div.tw-flex.tw-flex-row.tw-justify-end.tw-items-end.tw-mt-2.lg\:tw-mt-0.lg\:tw-pt-0.tw-space-x-reverse.tw-space-x-2.lg\:tw-min-h-\[4\.5rem\] > div.tw-flex.tw-flex-col.tw-items-center.tw-justify-between > span.tw-flex.tw-items-center.tw-font-bold.tw-text-base.lg\:tw-order-2 > span'
        )

        all_prices = [*prices, *discount_prices]

        images = soup.select(
            '#inspire > div > div.lg\:tw-mt-6 > div:nth-child(2) > div > div > div > main > div.tw-grid.tw-grid-cols-1.tw-mt-4.tw-gap-y-3.sm\:tw-grid-cols-2.sm\:tw-gap-3.lg\:tw-gap-4.lg\:tw-grid-cols-3.xl\:tw-grid-cols-4 > a > section > span > img'
        )

        for name, price, image in zip(names, all_prices, images):
            data.append(({
                'name': name.text.strip(),
                'price': int(price.text.strip().replace(',', '')),
            }, image.attrs['src']))

        page_number += 1
        if page_number > page_number_limit:
            crawl = False

    return data


def save_product_image(url, instance):
    response = requests.get(url)
    if not response.ok:
        return

    fp = BytesIO()
    fp.write(response.content)
    file_name = urlparse(url).path.replace('/', '-')
    instance.image.save(file_name, files.File(fp))
