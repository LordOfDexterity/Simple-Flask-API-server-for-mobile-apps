import json


def format_response(response):
    return json.dumps({'message': response})
