from xml import etree
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup

url = "https://www.bestbuy.com/site/aerial-drones-accessories/drones-with-cameras/pcmcat369900050002.c?id=pcmcat369900050002&intl=nosplash"
hdr = {'User-Agent': 'Mozilla/5.0'}
domain = "www.bestbuy.com"

response = requests.get(url, headers=hdr)
xml = ElementTree.ElementTree()
xml_parent = etree.Element('Products')
xml._setroot(xml_parent)

def parse_page():
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.findAll("li", {"class": "sku-item"})[:10]
    for item in products:
        parse_item(item)
    xml.write("sample.xml")


def parse_item(item):
    right_column = item.find("div", {"class": "right-column"})
    sku_header = right_column.find("h4", {"class": "sku-header"})
    product_name = sku_header.find("a").text
    product_link = sku_header.find("a", href=True)['href']

    review_block = right_column.find("div", {"class": "c-ratings-reviews-v2 ugc-ratings-reviews v-small"})
    review = review_block.find("p", {"class": "sr-only"}).text

    price_block = right_column.find("div", {"class": "price-block"})
    price_holder = price_block.find("div", {"class": "priceView-hero-price priceView-customer-price"})
    price = price_holder.find("span").text

    print(
        " Product: : " + product_name, "\n",
        "Link: " + "www.bestbuy.com" + product_link, "\n",
        "Review: " + review, "\n",
        "Price: " + price, "\n\n"
    )
    convert_to_xml(product_name, product_link, review, price)


def convert_to_xml(product_name,
                   product_link,
                   product_rating,
                   product_price):
    root = etree.Element('product')

    name = etree.Element('Name')
    name.text = product_name

    link = etree.Element('Link')
    link.text = product_link

    rating = etree.Element('Rating')
    rating.text = product_rating

    price = etree.Element('Price')
    price.text = product_price

    root.append(name)
    root.append(link)
    root.append(rating)
    root.append(price)
    xml_parent.append(root)


parse_page()
