from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, SelectField

class CouponForm(FlaskForm):
    user_id = StringField('Your ID')
    stake = FloatField('Stake')
    mode = SelectField('Recommendation mode', choices=[('high', 'High'), ('low', 'Low'), ('random', 'Random')], default='1')
    matches = IntegerField('Number of matches')
    submit = SubmitField('Get Coupon')