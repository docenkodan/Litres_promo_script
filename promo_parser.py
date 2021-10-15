import requests
from lxml import etree
from urllib.request import urlopen

PROMO_URL = 'https://lovikod.ru/knigi/promokody-litres'


def parse_promo():
    result = list()
    headers = {'Content-Type': 'text/html', }
    response = requests.get(PROMO_URL, headers=headers)

    html = response.text
    htmlparser = etree.HTMLParser()
    tree = etree.fromstring(html, htmlparser)
    table = tree.xpath('//*[@id="main"]/article/table[1]/tbody')
    for item in table[0]:
        item = item.find('.//strong')
        href = item.find('.//a').get("href")

        code_elem = item.find('.//span')
        if code_elem is None:
            code_elem = item.find('.//a')
        code = code_elem.text
        if 'автокод' in code:
            code = None
        result.append((code, href))
    return result



