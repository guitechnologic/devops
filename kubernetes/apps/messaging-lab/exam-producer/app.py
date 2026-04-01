import pika
import json
import time
import uuid
import random
import threading
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("exam-producer")

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

DEPARTMENTS = ["ER","ONC","PED","CAR","GEN"]
EXAMS = ["CBC","MRI","CT","XRAY","BIO"]

def generate_event():
    return {
        "exam_id": str(uuid.uuid4()),
        "department": random.choice(DEPARTMENTS),
        "exam": random.choice(EXAMS),
        "created_at": time.time()
    }

def producer_loop():
    while True:
        for _ in range(random.randint(5,15)):
            event = generate_event()

            channel.basic_publish(
                exchange="exam.exchange",
                routing_key="exam.created",
                body=json.dumps(event),
                properties=pika.BasicProperties(delivery_mode=2),
            )

            logger.info({"event":"published","exam":event["exam"]})

        time.sleep(random.randint(2,5))

threading.Thread(target=producer_loop).start()

while True:
    time.sleep(60)