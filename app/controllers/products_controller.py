from app.services.products_services import verify_products
def create_product():
  ...


def retrieve_products():
    ...


def product_by_id():
    ...


def update_product():
    ...


def delete_product(id):
    verify_products(id)
    current_app.db.session.delete(product)
    current_app.db.session.commit()
    