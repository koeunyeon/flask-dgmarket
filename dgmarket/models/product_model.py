from .. import db
from ..common.modelbase import ModelBase
from .enums import SellStatus

class Product(ModelBase):
    __tablename__ = 'products'

    seller_id = db.Column(db.Integer, nullable=False) # 판매자
    category_id = db.Column(db.Integer, nullable=False) # 카테고리
    title = db.Column(db.String(100), nullable=False) # 제목
    description = db.Column(db.Text, nullable=False) # 설명
    public_yn = db.Column(db.String(1), nullable=False, default='Y') # 공개여부.
    sell_status_id = db.Column(db.Integer, nullable=True, default=SellStatus.SELLING) # 판매 상태
    uplift_last_date = db.Column(db.DateTime, nullable=True) # 끌올 마지막 날짜
    uplift_count = db.Column(db.Integer, nullable=True, default=0) # 끌올 횟수
    uplift_last_discount_rate = db.Column(db.Integer, nullable=True, default=0) # 글올 마지막 할인율.