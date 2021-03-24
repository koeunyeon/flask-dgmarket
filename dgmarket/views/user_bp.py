from flask import Blueprint, request, render_template, abort

from ..models.user_model import User
from ..common import reswrap

from ..common import utils

bp = Blueprint('user', __name__, url_prefix='/user')

# 회원 가입 폼.
@bp.route("/regist", methods=["GET"])
def regist_form():
    return render_template("/user/regist.html")

# 회원 가입 처리
@bp.route("/regist", methods=['POST'])
def regist():
    data = request.get_json()
    login_email = data['login_email']
    nickname = data['nickname']

    if User.exist(login_email=login_email):
        # return abort(400, description="이미 존재하는 이메일입니다.")
        return reswrap.json_fail("이미 존재하는 이메일입니다.")

    if User.exist(nickname=nickname):
        # return abort(400, description="이미 존재하는 별명입니다.")
        return reswrap.json_fail("이미 존재하는 별명입니다.")

    user = User(login_email=login_email, nickname=nickname)
    user.regist_auth_key = utils.generate_random_key()    
    user.save()

    return reswrap.json_success(auth_key=user.regist_auth_key, user_id=user.id)

# 회원 가입 이메일 확인
@bp.route("/regist/verify/<user_id>/<regist_auth_key>", methods=['GET'])
def regist_verify(user_id, regist_auth_key):
    user = User.select(id=user_id, regist_auth_key=regist_auth_key).first()
    if user is None:
        return reswrap.json_fail("회원이 없습니다.")
    user.regist_auth_complete_yn = 'Y'
    user.save()

    return reswrap.json_success()
