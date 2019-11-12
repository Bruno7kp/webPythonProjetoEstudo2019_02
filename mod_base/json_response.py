from typing import List
from flask import jsonify
from mod_base.base import BaseModel


def json_response(message: str, data: List[BaseModel], redirect: str = None):
    return jsonify({
        'message': message,
        'data': [e.serialize() for e in data],
        'redirect': redirect
    })
