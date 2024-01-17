import json
from datetime import datetime
from catalog.models import Product, Category


def restore_data_from_json():
    with open('products_data.json', 'r') as json_file:
        data = json.load(json_file)

    for product_data in data:
        category_name = product_data['category']
        category, created = Category.objects.get_or_create(name=category_name)

        Product.objects.create(
            name=product_data['name'],
            description=product_data['description'],
            image=product_data['image'],
            category=category,
            price=float(product_data['price']),
            created_at=datetime.strptime(product_data['created_at'], '%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.strptime(product_data['updated_at'], '%Y-%m-%d %H:%M:%S'),
        )

    print('Data restored from products_data.json')


if __name__ == '__main__':
    restore_data_from_json()
