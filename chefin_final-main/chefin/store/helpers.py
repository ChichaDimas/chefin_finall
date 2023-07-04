
import requests
from django.core.files.base import ContentFile
from .models import Product
import os
from pprint import pprint


def get_menu_categories(api_key):
    url = 'https://joinposter.com/api/menu.getProducts'

    params = {
        'token': api_key,
        'format': 'json'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get('response', [])


def fill_database(api_key):
    url = 'https://joinposter.com/api/menu.getProducts'

    params = {
        'token': api_key,
        'format': 'json'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err}")
        return

    if response.status_code == 200:
        # Delete existing categories
        Product.objects.all().delete()

        categories = get_menu_categories(api_key)

        for category in categories:
            # Create new categories

            # Create new products
            try:
                price = list(category.get('price', {}).values())[0]
                price_for_view = f"{price[:-2]}.{price[-2:]}"
                product, created = Product.objects.get_or_create(
                    name=category.get('product_name'),
                    category=category.get('category_name'),
                    description=category.get('product_production_description'),
                    price=price,
                    price_for_view=price_for_view,
                    image=f"https://joinposter.com{category.get('photo', '')}",

                    product_id=category.get('product_id'),
                )
                # product_id = category.get('product_id')
                # print(product_id)
            except Exception as err:
                print(f"Error: {err}")
                continue