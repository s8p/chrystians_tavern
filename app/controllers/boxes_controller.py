from http import HTTPStatus

from flask import jsonify
from app.services import boxes_services


def create_box():
    ...


def retrieve_boxes():
    return (jsonify(boxes_services.get_all_boxes()), HTTPStatus.OK)


def retrieve_box_flag():
    ...


def update_box():
    ...


def delete_box():
    ...
