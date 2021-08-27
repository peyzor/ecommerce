import requests

from bs4 import BeautifulSoup


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
            '#inspire > div > div:nth-child(2) > div.lg\:tw-bg-gray-100 > div > div > main > div.tw-grid.tw-grid-cols-1.tw-mt-4.tw-gap-y-3.sm\:tw-grid-cols-2.sm\:tw-gap-3.lg\:tw-gap-4.lg\:tw-grid-cols-3.xl\:tw-grid-cols-4 > a > section > div > h4 > span'
        )

        prices = soup.select(
            '#inspire > div > div:nth-child(2) > div.lg\:tw-bg-gray-100 > div > div > main > div.tw-grid.tw-grid-cols-1.tw-mt-4.tw-gap-y-3.sm\:tw-grid-cols-2.sm\:tw-gap-3.lg\:tw-gap-4.lg\:tw-grid-cols-3.xl\:tw-grid-cols-4 > a > section > div > div > div.tw-flex.tw-flex-row.tw-justify-end.tw-items-end.tw-mt-2.lg\:tw-mt-4.lg\:tw-pt-4.tw-space-x-reverse.tw-space-x-2.lg\:tw-min-h-\[5\.0625rem\] > div.tw-flex.tw-flex-col.tw-items-center.tw-justify-center > span.tw-flex.tw-items-center.tw-text-sm.lg\:tw-text-xl.lg\:tw-order-2.tw-font-bold > span'
        )

        discount_prices = soup.select(
            '#inspire > div > div:nth-child(2) > div.lg\:tw-bg-gray-100 > div > div > main > div.tw-grid.tw-grid-cols-1.tw-mt-4.tw-gap-y-3.sm\:tw-grid-cols-2.sm\:tw-gap-3.lg\:tw-gap-4.lg\:tw-grid-cols-3.xl\:tw-grid-cols-4 > a > section > div > div > div.tw-flex.tw-flex-row.tw-justify-end.tw-items-end.tw-mt-2.lg\:tw-mt-4.lg\:tw-pt-4.tw-space-x-reverse.tw-space-x-2.lg\:tw-min-h-\[5\.0625rem\] > div.tw-flex.tw-flex-col.tw-items-center.tw-justify-between > span.tw-flex.tw-items-center.tw-text-sm.lg\:tw-text-xl.lg\:tw-order-2.tw-font-bold > span'
        )

        all_prices = [*prices, *discount_prices]

        for name, price in zip(names, all_prices):
            data.append({
                'name': name.text.strip(),
                'price': int(price.text.strip().replace(',', ''))
            })

        page_number += 1
        if page_number > page_number_limit:
            crawl = False

    return data
