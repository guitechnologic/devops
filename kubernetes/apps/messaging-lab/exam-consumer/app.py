import pika, json, time, random, logging
from prometheus_client import Counter, start_http_server

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("exam-consumer")

RABBITMQ_HOST = "rabbitmq.messaging.svc.cluster.local"
MESSAGES_CONSUMED = Counter("exam_messages_consumed_total","messages")

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

def callback(ch, method, properties, body):
    event = json.loads(body)
    logger.info({"event":"received","exam":event["exam"]})
    time.sleep(random.uniform(0.5,2.0))
    logger.info({"event":"processed","exam":event["exam"]})
    MESSAGES_CONSUMED.inc()
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="exam.requests", on_message_callback=callback)

start_http_server(8000)
channel.start_consuming()
