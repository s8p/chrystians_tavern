from app.configs.database import db
from app.models import ProductModel, CategoriesModel
from app.exceptions.product_exc import ProductNotFound, InvalidValues, WrongKeys

from sqlalchemy.orm.session import Session


def verify_data(data: dict):
    if not data.get('available_amount'):
        data['available_amount'] = 0

    data_keys = set(data.keys())
    default_keys = set(["name", "price", "category", 'available_amount'])

    if data_keys != default_keys:
        raise WrongKeys

    price_key = data["price"]
    
    if price_key <= 25000:
        data["flag"] = "Bronze"

    elif price_key > 25000 and price_key <= 50000:
        data["flag"] = "Silver"

    elif price_key > 50000:
        data["flag"] = "Gold"
    
    data["category"] = data["category"].capitalize()

    if type(data["category"]) != str or type(data["name"]) != str:
        raise InvalidValues

    if type(data["price"]) != int or type(data["available_amount"]) != int:
        raise InvalidValues

    return data


def check_category(data: dict):
    session: Session = db.session

    category_name = data["category"]

    category = CategoriesModel.query.get(category_name)

    if not category:
        category_data = {"name": category_name}

        category = CategoriesModel(**category_data)

        session.add(category)
        session.commit()


def verify_product(product_id: int):
    session: Session = db.session

    product = session.query(ProductModel).get(product_id)

    if not product:
        raise ProductNotFound

    return product


def check_keys(data: dict):
    category = data.get("category")

    if category:
        data["category"] = data["category"].capitalize()

    default_keys = ["name", "price", "category", "available_amount"]

    data_keys = list(data.keys())

    for key in data_keys:
        if key not in default_keys:
            raise WrongKeys

        if key == "category" or key == "name":
            if type(data[key]) != str:
                raise InvalidValues

        elif key == "price" or key == "available_amount":
            if type(data[key]) != int:
                raise InvalidValues

    return data
