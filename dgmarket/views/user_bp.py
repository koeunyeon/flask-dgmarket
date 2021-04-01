import datetime
from flask import Blueprint, request, render_template, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

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

    user = User()
    user.regist(login_email, nickname)

    return reswrap.json_success(auth_key=user.regist_auth_key, user_id=user.id)


# 회원 가입 이메일 확인
@bp.route("/regist/verify/<user_id>/<regist_auth_key>", methods=['GET'])
def regist_verify(user_id, regist_auth_key):
    user = User.select(id=user_id, regist_auth_key=regist_auth_key).first()
    if user is None:
        return reswrap.json_fail("회원이 없습니다.")
    
    user.regist_verify()
    return reswrap.json_success()


# 로그인 폼
@bp.route("/login", methods=["GET"])
def login_form():
    return render_template("/user/login.html")

# 로그인 인증키 발송. 원칙대로라면 이메일을 보낸다. 지금 버전은 그냥 JSON 리턴함.
@bp.route("/login", methods=["POST"])
def login_send_auth_key():
    data = request.get_json()
    login_email = data['login_email']
    user = User.first(login_email=login_email, regist_auth_complete_yn='Y')
    if user is None:
        return reswrap.json_fail("이메일이 없습니다.")
    
    user.login_send_auth_key()

    expired_date = user.login_auth_send_date + datetime.timedelta(hours=2) # 2시간 유효
    expired_message = "이 링크는 " + expired_date.strftime("%Y년 %m월 %d일 %H시 %M분 %S초") + " 까지 유효합니다."

    return reswrap.json_success(auth_key=user.login_auth_key, user_id=user.id, expired_date=expired_date.strftime("%Y%m%d%H%M%S"), expired_message=expired_message)
    

# 실제 로그인 처리. JWT 리턴함.
@bp.route("/login/verify/<user_id>/<login_auth_key>", methods=['GET'])
def login_auth(user_id, login_auth_key):
    user = User.select(id=user_id, login_auth_key=login_auth_key).first()
    if user is None:
        return reswrap.json_fail("로그인에 실패했습니다.")
    
    # 시간 만료 체크
    expired_date = user.login_auth_send_date + datetime.timedelta(hours=2)
    expired_date = float(expired_date.strftime("%Y%m%d%H%M%S"))

    now_date = datetime.datetime.now()
    now_date = float(now_date.strftime("%Y%m%d%H%M%S"))
    if now_date > expired_date:
        return reswrap.json_fail("로그인 시간이 만료되었습니다.")

    access_token = create_access_token(identity=user.id, expires_delta=False) # expires_delta == False. 무제한.    
    return reswrap.json_success(token=access_token)

# 로그인 가능 여부 JWT 토큰 검증
@bp.route("/login/check")
@jwt_required()
def login_check():
    cur_user = get_jwt_identity()
    if cur_user is None:
        return reswrap.json_fail("토큰이 정상이 아닙니다.")

    return reswrap.json_success(user = cur_user)