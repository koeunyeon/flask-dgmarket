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

    @classmethod
    def exist_login_email(cls, login_email):
        return cls.exist(login_email=login_email)

    @classmethod
    def exist_nickname(cls, nickname):
        return cls.exist(nickname=nickname)

    def regist(self):
        self.regist_auth_key = utils.generate_random_key(10)
        return self
