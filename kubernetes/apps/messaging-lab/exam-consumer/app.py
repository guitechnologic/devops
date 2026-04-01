import pika
import json
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("exam-consumer")

RABBITMQ_HOST = "rabbitmq.messaging.svc.cluster.local"

credentials = pika.PlainCredentials("devops", "devops123")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=credentials
    )
)
channel = connection.channel()

channel.exchange_declare(exchange="exam.exchange", exchange_type="direct")
channel.queue_declare(queue="exam.requests", durable=True)
channel.queue_bind(
    exchange="exam.exchange",
    queue="exam.requests",
    routing_key="exam.created"
)

def callback(ch, method, properties, body):
    event = json.loads(body)

    logger.info({"event":"received","exam":event["exam"]})
    time.sleep(random.uniform(0.5,2.0))
    logger.info({"event":"processed","exam":event["exam"]})

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="exam.requests", on_message_callback=callback)

logger.info("Waiting for messages...")
channel.start_consuming()
