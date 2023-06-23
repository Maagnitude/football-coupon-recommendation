import pika
import json
from recommendationapp.funcs import create_coupon
from recommendationapp import app, db
from sqlalchemy.orm import sessionmaker
import os

amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

# CONSUMER
print(' Connecting to server ...')

try:
    # With docker
    connection = pika.BlockingConnection(url_params)
    # Without docker
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", port=5672, virtual_host="/", credentials=pika.PlainCredentials("guest", "guest")))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")

channel = connection.channel()
channel.queue_declare(queue='coupon_queue', durable=True)

print(' Waiting for messages...')

def callback(ch, method, properties, body):
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()
        coupons, code = create_coupon(json.loads(body), session)
        session.close()
        print(" Received %s" % coupons)
        print(" Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

# to make sure the consumer receives only one message at a time
# next message is received only after acking the previous one
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='coupon_queue', on_message_callback=callback)
channel.start_consuming()