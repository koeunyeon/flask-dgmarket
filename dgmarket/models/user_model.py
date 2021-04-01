import datetime

from .. import db
from ..common.modelbase import ModelBase
from ..common import utils


class User(ModelBase):
    __tablename__ = 'users'
    login_email = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    regist_auth_key = db.Column(db.String(10))  # 인증키
    # 인증키 보낸 시간.
    regist_auth_send_date = db.Column(
        db.DateTime, default=datetime.datetime.now)
    # 회원 가입 인증 완료.
    regist_auth_complete_yn = db.Column(db.String(1), default='N')

    # 로그인 임시 키
    login_auth_key = db.Column(db.String(15))
    
    # 로그인키 보낸 시간.
    login_auth_send_date = db.Column(db.DateTime)

    # 회원가입
    def regist(self, login_email, nickname):
        self.login_email = login_email
        self.nickname = nickname
        self.regist_auth_key = utils.generate_random_key()
        self.save()
    
    # 회원 가입 이메일 확인
    def regist_verify(self):
        self.regist_auth_complete_yn = 'Y'
        self.save()

    # 로그인 인증키 발송
    def login_send_auth_key(self):
        self.login_auth_key = utils.generate_random_key(15)
        self.login_auth_send_date = datetime.datetime.now()
        self.save()

    # 로그인 인증키 시간 경과 여부 확인
    def is_login_auth_expired(self):        
        expired_date = self.login_auth_send_date + datetime.timedelta(hours=2)
        expired_date = float(expired_date.strftime("%Y%m%d%H%M%S"))

        now_date = datetime.datetime.now()
        now_date = float(now_date.strftime("%Y%m%d%H%M%S"))
        return now_date > expired_date
        
            
