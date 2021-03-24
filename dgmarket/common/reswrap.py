from flask import jsonify, abort

def json_success(**kwargs):
    kwargs['result'] = True
    return jsonify(kwargs)

def json_fail(message):
    return abort(400, description=message)
    