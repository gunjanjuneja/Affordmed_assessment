from flask import Flask, request, jsonify
from utils.ecommerce_api import fetch_products
from utils.config import COMPANIES, MAX_PRODUCTS_PER_PAGE

app = Flask(__name__)

def generate_product_id(product, company):
    return f"{company}_{product['productName'].replace(' ', '_')}"

@app.route('/categories/<category>/products', methods=['GET'])
def get_top_products(category):
    n = int(request.args.get('n', 10))
    min_price = float(request.args.get('minPrice', 0))
    max_price = float(request.args.get('maxPrice', float('inf')))
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))

    print(f"Fetching products for category: {category}")
    all_products = []
    for company in COMPANIES:
        products = fetch_products(company, category, n, min_price, max_price)
        print(f"Fetched {len(products)} products from {company}")
        for product in products:
            product['id'] = generate_product_id(product, company)
            product['company'] = company
        all_products.extend(products)
    
    print(f"Total products fetched: {len(all_products)}")
    if sort_by:
        reverse = (order == 'desc')
        all_products = sorted(all_products, key=lambda x: x.get(sort_by, 0), reverse=reverse)

    start = (page - 1) * MAX_PRODUCTS_PER_PAGE
    end = start + MAX_PRODUCTS_PER_PAGE
    paginated_products = all_products[start:end]

    return jsonify(paginated_products)

@app.route('/categories/<category>/products/<product_id>', methods=['GET'])
def get_product_details(category, product_id):
    for company in COMPANIES:
        products = fetch_products(company, category, 10, 0, float('inf'))  # Fetch a reasonable number
        for product in products:
            if generate_product_id(product, company) == product_id:
                product['id'] = generate_product_id(product, company)
                product['company'] = company
                return jsonify(product)
    return jsonify({"message": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
