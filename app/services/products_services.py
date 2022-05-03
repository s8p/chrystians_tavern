
from flask import current_app
from app.exceptions.product_exc import ProductNotFound
from app.models import ProductModel


# criar produtos
def post_product():
    data = request.get_json()
    products = ProductModel(**data)
    return products



# mostrar todos produtos
def get_product():
    data = ProductModel.query.all()
    serializer = [
        {
            "id": data.id,
            "name": data.name,
            "price": data.price,
            "category": data.category,
            "available_amount": data.available_amount,
            "flag": data.flag
        } for data in data
    ]
    return serializer



# verificar id dos produtos
def verify_products(product_id):
    current_app.db.session()
    product = ProductModel.query.get(product_id)

    if not product:
        raise ProductNotFound

    return product
    
    


