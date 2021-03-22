from flask import Blueprint, request, render_template, abort

from ..models.user_model import User
from ..common import reswrap


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/regist", methods=["GET"])
def regist_form():
    return render_template("/user/regist.html")

@bp.route("/regist", methods=['POST'])
def regist():
    data = request.get_json()
    login_email = data['login_email']
    nickname = data['nickname']

    if User.exist_login_email(login_email):
        return abort(400, description="이미 존재하는 이메일입니다.")

    if User.exist_nickname(nickname):
        return abort(400, description="이미 존재하는 별명입니다.")

    user = User(login_email=login_email, nickname=nickname)
    user.regist()
    user.save()

    return reswrap.json_success(auth_key=user.regist_auth_key)
