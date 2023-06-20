from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from recommendationapp.funcs import create_coupon, find_all_events
from recommendationapp import db
from sqlalchemy.orm import sessionmaker
from recommendationapp.coupons.forms import CouponForm

coupons = Blueprint('coupons', __name__, template_folder='templates/coupons')

@coupons.route('/api/coupons', methods=['GET', 'POST'])
def api_get_coupon():
    user_info = request.get_json()
    if request.method == 'POST':
        Session = sessionmaker(bind=db.engine)
        batch_session = Session()
        coupon, code = create_coupon(user_info, batch_session)
        batch_session.close()
        return jsonify(code, coupon)
    return jsonify(user_info)

@coupons.route('/coupons', methods=['GET', 'POST'])
def get_coupon():
    form = CouponForm()
    
    if form.validate_on_submit():
        
        user_id = form.user_id.data
        matches = form.matches.data
        stake = form.stake.data
        mode = form.mode.data
        
        user_info = {
            'user_id': user_id,
            'stake': stake,
            'mode': mode,
            'matches': matches
        }
        Session = sessionmaker(bind=db.engine)
        batch_session = Session()
        
        coupon, code = create_coupon(user_info, batch_session)
        if code == 400:
            return redirect(url_for('core.index'))
        events = find_all_events()[0]
        
        batch_session.close()
        return render_template('got_coupon.html', coupon=coupon, code=code, events=events)
    return render_template('coupons.html', form=form)