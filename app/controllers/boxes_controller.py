from http import HTTPStatus

from flask import jsonify
from app.services import boxes_services


def create_box():
    return (jsonify(boxes_services.add_box()), HTTPStatus.CREATED)


def retrieve_boxes():
    return (jsonify(boxes_services.get_all_boxes()), HTTPStatus.OK)


def retrieve_box_flag():
    return boxes_services.get_one_box()


def update_box():
    ...


def delete_box(box_flag: str):
    return boxes_services.delelete_by_flag(box_flag)
