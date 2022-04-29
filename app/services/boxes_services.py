import locale

from app.models.boxes_model import BoxesModel

locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")

from app.configs.database import db
from sqlalchemy.orm import Session

def get_all_boxes():
	session: Session = db.session
	boxes = session.query(BoxesModel).all()
	return boxes