from flask import render_template, request, Blueprint
from recommendationapp.funcs import get_a_coupon, create_coupon

coupons = Blueprint('coupons', __name__)

@coupons.route('/coupons', methods=['GET', 'POST'])
def get_coupon():
    
    if request.method == 'GET':
        user, coupon, events = get_a_coupon()
        return render_template('coupons.html', user=user, coupon=coupon, events=events)
    else: 
        coupon, code = create_coupon()
        return coupon, code