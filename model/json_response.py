from typing import List
from model.base import BaseModel


def json_response(message: str, data: List[BaseModel], redirect: str = None):
    return {
        'message': message,
        'data': [e.serialize() for e in data],
        'redirect': redirect
    }
