from http import HTTPStatus
from flask import request, jsonify, current_app
from app.exceptions.product_exc import ProductNotFound
from app.models.products_model import ProductModel


def update_products(id):
    ...

def verify_products(id):
    product = ProductModel.query.get(id)

    if(not product):
        raise ProductNotFound

       
    
    


