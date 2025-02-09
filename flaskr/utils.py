
from flask import (
    Blueprint, request
)
from .errors import *


def get_params(param) -> list:
    args = request.args.getlist(param)
    if not args:
        return []
    return args
    
def get_json_body(*keys) -> dict:
    data = request.get_json()
    response = {}
    for key in keys:
        new_content = data.get(key)
        if new_content is None:
            raise RequestJSONBodyError(key)
        response[key] = new_content
    return response
