from fastapi import FastAPI
import requests
import random
import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from otel import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# --------- INIT ---------
setup_tracing()

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pt-clinic")

app = FastAPI(title="EU Health Interoperability Simulator")
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

GATEWAY_URL = "http://eu-gateway:8000/exchange"

DEPARTMENTS = ["ER", "ONC", "PED", "CAR", "GEN"]
EXAMS = ["CBC", "MRI", "CT", "XRAY", "BIO"]

executor = ThreadPoolExecutor(max_workers=50)

def simulate_consultation():
    department = random.choice(DEPARTMENTS)
    exam = random.choice(EXAMS)

    payload = {
        "department": department,
        "exam": exam
    }

    try:
        response = requests.post(GATEWAY_URL, json=payload, timeout=5)

        logger.info({
            "service": "pt-clinic",
            "event": "consultation_completed",
            "status": response.status_code
        })

    except Exception as e:
        logger.error({
            "service": "pt-clinic",
            "event": "consultation_failed",
            "error": str(e)
        })

def traffic_generator():
    while True:
        for _ in range(random.randint(5, 20)):
            executor.submit(simulate_consultation)
        time.sleep(random.uniform(2, 5))

@app.on_event("startup")
def start_traffic():
    threading.Thread(target=traffic_generator, daemon=True).start()
