from werkzeug.exceptions import HTTPException


class RequestJSONBodyError(HTTPException):
    code = 400
    description = "Error in JSON body passed to request."

    def __init__(self, key, *args, **kwargs):
        super().__init__(self, key, *args, **kwargs)
        self.key = key 
        self.description = f"Error in JSON body passed to request.  Can not read access key: {key}"
        
class RecordAlreadyExists(HTTPException):
    code = 400
    description = "A record with this data already exists."

    def __init__(self, key, *args, **kwargs):
        super().__init__(self, key, *args, **kwargs)
        self.key = key 
        self.description = f"A record with the data '{key}' already exists."

def handle_bad_json_body_error(e):
    response = {
        'error': 'RequestJSONBodyError',
        'description': e.description,
        'status_code': 400
    }
    return response

def handle_record_already_exists_error(e):
    response = {
        'error': 'RecordAlreadyExists',
        'description': e.description,
        'status_code': 400
    }
    return response
