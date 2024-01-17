import json
from catalog.models import Product


def save_data_to_json():
    products = Product.objects.all()

    data = []

    for product in products:
        product_data = {
            'name': product.name,
            'description': product.description,
            'image': str(product.image),
            'category': product.category.name,
            'price': str(product.price),
            'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': product.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        data.append(product_data)

    with open('products_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print('Data saved to products_data.json')


if __name__ == '__main__':
    save_data_to_json()
