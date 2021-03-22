from flask import jsonify


def response_not_found(e):
    return jsonify({'result': False, 'message': str(e)}), 400
