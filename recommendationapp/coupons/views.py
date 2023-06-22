from flask import render_template, request, Blueprint, jsonify
from recommendationapp.funcs import create_coupon, find_all_events, find_coupons
from recommendationapp import db
from sqlalchemy.orm import sessionmaker
from recommendationapp.coupons.forms import CouponForm, MyCouponForm
import pika, json

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
        
        coupons, code = create_coupon(user_info)
        if code == 400:
            return render_template('coupons.html', form=form, code=code)
        events = find_all_events()[0]
        
        if coupons is not list:
            coupons = [coupons]
        from_form = 1
        return render_template('got_coupon.html', coupons=coupons, code=code, events=events, from_form=from_form)
    return render_template('coupons.html', form=form)

@coupons.route('/got_coupon', methods=['GET', 'POST'])
def got_coupon():
    form = MyCouponForm()
    
    if form.validate_on_submit():
        user_id = form.user_id.data
    
        coupons, code = find_coupons(user_id)
        if code == 400:
            return render_template('show_my_coupons.html', form=form, code=code)
        events = find_all_events()[0]
        if coupons is None:
            return render_template('got_coupon.html', coupons=None)
        from_form = 0
        return render_template('got_coupon.html', coupons=coupons, events=events, from_form=from_form)
    return render_template('show_my_coupons.html', form=form)

# PRODUCER
@coupons.route('/testcoupon', methods=['GET', 'POST'])
def coupon_test():
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
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, virtual_host="/", credentials=pika.PlainCredentials("kazazis", "1234")))
        except pika.exceptions.AMQPConnectionError as exc:
            print("Failed to connect to RabbitMQ service. Message wont be sent.")
            return

        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=json.dumps(user_info),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
    return render_template('coupons.html', form=form)