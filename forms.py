"""フォーム定義"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DateField,
    TextAreaField,
    SubmitField,
    SelectField,
    HiddenField,
)
from wtforms.validators import DataRequired, NumberRange, Optional


class OrderForm(FlaskForm):
    customer_name = StringField("Customer Name", validators=[DataRequired()])
    product_id = SelectField("Product", coerce=int, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    desired_date = DateField("Desired Date", validators=[Optional()])
    note = TextAreaField("Note", validators=[Optional()])
    submit = SubmitField("Save")


class RestockForm(FlaskForm):
    product_id = HiddenField("Product ID", validators=[DataRequired()])
    amount = IntegerField("Amount", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("補充")


class ProductForm(FlaskForm):
    name = StringField("商品名", validators=[DataRequired()])
    price = IntegerField("価格", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("商品を追加")
