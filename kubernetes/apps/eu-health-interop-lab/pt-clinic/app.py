from fastapi import FastAPI
import requests
import random
import time
import logging

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("pt-clinic")

app = FastAPI(title="PT Health Clinic")
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

DEPARTMENTS = ["ER", "ONC", "PED", "CAR", "GEN"]
EXAMS = ["CBC", "MRI", "CT", "XRAY", "BIO"]

@app.post("/consultation")
def start_consultation():
    department = random.choice(DEPARTMENTS)
    exam = random.choice(EXAMS)

    payload = {
        "patient_id": f"pt-{random.randint(1000,9999)}",
        "department": department,
        "exam": exam,
        "origin": "PT"
    }

    logger.info({
        "service": "pt-clinic",
        "event": "consultation_started",
        "department": department,
        "exam": exam
    })

    response = requests.post(
        "http://eu-gateway:8000/exchange",
        json=payload,
        timeout=5
    )

    return response.json()
