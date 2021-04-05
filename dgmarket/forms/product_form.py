from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, validators

class ProductForm(FlaskForm):
    seller_id = IntegerField(label="seller id", validators=[validators.DataRequired()]) # Required()는 Wtforms 3.0 부터. 2.x 에서는 DataRequired 
    category_id = IntegerField(label="category id", validators=[validators.DataRequired()])
    title = StringField(label="title", validators=[validators.length(min=4,max=60)])
    description = StringField(label="description", validators=[validators.DataRequired()])