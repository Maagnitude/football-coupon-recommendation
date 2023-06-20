from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField

class CouponForm(FlaskForm):
    user_id = StringField('Your ID')
    stake = FloatField('Stake')
    mode = StringField('Recommendation mode')
    matches = IntegerField('Number of matches')
    submit = SubmitField('Get Coupon')