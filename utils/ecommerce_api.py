import requests
import requests
from .config import BASE_URL, AUTH_TOKEN

import requests
from .config import BASE_URL, AUTH_TOKEN

def fetch_products(company, category, top, min_price, max_price):
    url = f"{BASE_URL}/{company}/categories/{category}/products"
    params = {
        "top": top,
        "minPrice": min_price,
        "maxPrice": max_price
    }
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        products = response.json()
        if isinstance(products, list):
            return products
        else:
            print("Invalid response format. Expected a list.")
            return []
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
        return []



def generate_product_id(product, company):
    import hashlib
    unique_string = f"{company}-{product['productName']}-{product['price']}"
    return hashlib.md5(unique_string.encode()).hexdigest()
