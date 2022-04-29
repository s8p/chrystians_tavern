import locale
from app.models.boxes_model import BoxesModel
from app.configs.database import db
from sqlalchemy.orm import Session


locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")



def get_all_boxes():
	session: Session = db.session
	boxes = session.query(BoxesModel).all()
	adapted_boxes = []
	for boxe in boxes:
		adapted_box = dict(**boxe.__dict__)
		adapted_box.pop("_sa_instance_state")
		adapted_box.update({"monthly_price":locale.currency(boxe.monthly_price)})
		adapted_boxes.append(adapted_box)
	return adapted_boxes
