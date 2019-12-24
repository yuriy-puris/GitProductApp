import requests

from bs4 import BeautifulSoup
from lxml import html
import lxml.etree

from . import service_headers
  
COUNT_PRODUCTS_SHOP = 5

SHOPS_PRODUCT_LIST_CLASSES = {
  1: 'catalog__main-content',
  2: 'product-tile_container',
  4: 'category-products',
  5: 'listing-container'
}

def get_response(url):
  try:
    response = requests.get(url, headers=service_headers.headers['2'])
    print(url)
    return response.text
  except ValueError:
    return None


def get_category(shop_id, html):
  soup = BeautifulSoup(html, 'html.parser')
  soup.prettify()
  try:
    content_wrap = soup.find(True, class_=SHOPS_PRODUCT_LIST_CLASSES[shop_id])
    return content_wrap
  except:
    return None


def parse_product_list(shop_id, content, host):
  if shop_id == 1:
    return get_product_list_shop_1(shop_id, content, host)
  if shop_id == 2:
    return get_product_list_shop_2(shop_id, content, host)
  if shop_id == 4:
    return get_product_list_shop_4(shop_id, content, host)
  if shop_id == 5:
    return get_product_list_shop_5(shop_id, content, host)

def get_product_list_shop_4(shop_id, content, host):
  try:
    grid_list = content.find_all('li', class_='item')
    products = []

    for item in grid_list[:COUNT_PRODUCTS_SHOP]:
      img_block = item.find('div', class_='item-picture-blk')
      img = img_block.find('img').attrs
      img_url = img['data-original']
      link = img_block.find('a', class_='product-image').attrs
      _url = link['href']
      title = item.find_all('div', class_='product-name-container')[0].text.strip()
      price = item.find('span', class_='sum').text.strip().replace(u"\xa0", u".")
      product = {
        'shop_id': shop_id,
        'img':   img_url,
        'title': title,
        'price': price,
        'url': 'https:' + _url
      }
      products.append(product)

    return products
  except ValueError:
    return None

def get_product_list_shop_5(shop_id, content, host):
  try:
    grid_list = content.find_all('div', class_=['listing-item', 'product-item', 'simple'])
    products = []

    for item in grid_list[:COUNT_PRODUCTS_SHOP]:
      item_attrs = item.attrs
      if item.find('img', class_='lazy-category') is not None:
        item_img = item.find('img', class_='lazy-category').attrs
        img = item_img['data-src']
        title = item_attrs['data-title']
        price = item_attrs['data-price']
        _url = item_attrs['data-url']
        product = {
          'shop_id': shop_id,
          'img':   img,
          'title': title,
          'price': price,
          'url': host + _url
        }

        products.append(product)
    return products
  except ValueError:
    return None

def get_product_list_shop_2(shop_id, content, host):
  try:
    grid_list = content.find_all('section', class_='product-tile_product')
    products = []

    for item in grid_list[:COUNT_PRODUCTS_SHOP]:
      item_attrs = item.attrs
      img_attrs = item.find('figure', class_='goods_image').attrs
      img = img_attrs['data-imagesrc']
      title = item_attrs['data-name']
      price = item_attrs['data-price']
      _url = item_attrs['data-href']
      product = {
        'shop_id': shop_id,
        'img':   img,
        'title': title,
        'price': price,
        'url': host + _url
      }

      products.append(product)
    return products
  except ValueError:
    return None

def get_product_list_shop_1(shop_id, content, host):
  try:
    grid_list = content.find_all('div', class_='catalog-item product-card__')
    products = []

    for item in grid_list[:COUNT_PRODUCTS_SHOP]:
      img_attrs = item.find('img', class_='product-img').attrs
      img = img_attrs['data-src']
      title_link = item.find('div', class_='title-itm')
      title = item.find('h5').text.strip()
      price = item.find('span', class_='price-number').text.strip()
      _url_attr = item.find('a', class_='card-product-link').attrs
      _url = _url_attr['href']
      product = {
        'shop_id': shop_id,
        'img':   img,
        'title': title,
        'price': price,
        'url': host + _url
      }

      products.append(product)
    return products
  except ValueError:
    return None

def parse_shop(shop_id, url, host):
  try:
    html = get_response(url)
    if html is None:
      print('ConnectionError')
      raise ConnectionError('ConnectionError') 
    content_products = get_category(shop_id, html)
    if content_products is None:
      print('Content products isn\'t found')
      raise ValueError('Content products isn\'t found')
    parse_products = parse_product_list(shop_id, content_products, host)
    if content_products is None:
      print(f'Problem with parser {shop_id}')
      raise ValueError('Problem with parser')
    return parse_products
    
  except ConnectionError:
    return []
  except ValueError: 
    return []  
    