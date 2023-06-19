from flask import render_template, request, Blueprint, jsonify
from recommendationapp.funcs import get_a_coupon, create_coupon
from recommendationapp import db
from sqlalchemy.orm import sessionmaker

coupons = Blueprint('coupons', __name__)

@coupons.route('/coupons', methods=['GET', 'POST'])
def get_coupon():
    user_info = request.get_json()
    if request.method == 'POST':
        Session = sessionmaker(bind=db.engine)
        batch_session = Session()
        coupon, code = create_coupon(user_info, batch_session)
        print(coupon)
        batch_session.close()
        return jsonify(code)
        # return render_template('coupons.html', user=user, coupon=coupon, events=events)
    # else: 
        # coupon, code = get_a_coupon(user_info)
        # return coupon, code
    
    #POST, θα δεχετε χρηστη και stake, θα επιστρεφει το coupon με τα αντιστοιχα odds
    # INPUT: mode- high, low, random | stake | user | number of matches
    #              high: θα επιλεγει τα ακριβοτερα odds