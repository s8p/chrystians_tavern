from flask import current_app, request, jsonify
from app.exceptions.product_exc import ProductNotFound
from app.models import ProductModel, CategoriesModel




def post_product(data):
    
    if type(data["category"]) and type(data["name"]) != str:
        return jsonify({'error':'Unexpected shape'})
    if type(data["price"]) and type(data["available_amount"]) != int:
        return jsonify({'error':'Unexpected shape'})
    products = ProductModel(**data)
    return products


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




def verify_products(product_id):
    current_app.db.session()
    product = ProductModel.query.get(product_id)

    if not product:
        raise ProductNotFound

    return product


def check_category(data):
    current_app.db.session()
    category = CategoriesModel.query.get(data["category"])
    if not category:
        category_data = {'name':data["category"]}
        current_app.db.session.add(category_data)
        current_app.db.session.commit()
    print(data)
    print(category)
    