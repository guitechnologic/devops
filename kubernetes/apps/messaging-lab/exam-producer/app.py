import pika, json, time, uuid, random, threading, logging, os
from fastapi import FastAPI
from prometheus_client import Counter, start_http_server

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("exam-producer")

RABBITMQ_HOST = "rabbitmq.messaging.svc.cluster.local"

MESSAGES_PUBLISHED = Counter("exam_messages_published_total","messages")

def connect():
    while True:
        try:
            credentials = pika.PlainCredentials("devops","devops123")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            )
            logger.info("connected_to_rabbitmq")
            return connection.channel()
        except Exception as e:
            logger.info({"event":"rabbit_retry","error":str(e)})
            time.sleep(5)

channel = connect()
channel.exchange_declare(exchange="exam.exchange", exchange_type="direct")
channel.queue_declare(queue="exam.requests", durable=True)
channel.queue_bind(exchange="exam.exchange",queue="exam.requests",routing_key="exam.created")

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
            MESSAGES_PUBLISHED.inc()
            logger.info({"event":"published","exam":event["exam"]})
        time.sleep(random.randint(2,5))

threading.Thread(target=producer_loop, daemon=True).start()

# metrics server
start_http_server(8000)

while True:
    time.sleep(60)
    