import pika
import json
from recommendationapp.funcs import create_coupon
from recommendationapp import app, db
from sqlalchemy.orm import sessionmaker

# CONSUMER
print(' Connecting to server ...')

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, virtual_host="/", credentials=pika.PlainCredentials("kazazis", "1234")))
except pika.exceptions.AMQPConnectionError as exc:
    print("Failed to connect to RabbitMQ service. Message wont be sent.")

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

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

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()