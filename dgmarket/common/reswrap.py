from flask import jsonify
def json_success(**kwargs):
    kwargs['result'] = True
    return jsonify(kwargs)