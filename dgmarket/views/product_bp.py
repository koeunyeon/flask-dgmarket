from flask import Blueprint, request, abort

from ..forms.product_form import ProductForm

bp = Blueprint('product', __name__, url_prefix='/product')



# 상품 등록
@bp.route("/enroll", methods=['GET', 'POST'])
def enroll():    
    data = request.get_json()          
    form = ProductForm.from_json(data)    
    return dict(data=form.seller_id.data)