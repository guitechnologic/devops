from fastapi import FastAPI
import requests
import logging
import time

from otel import setup_tracing
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# --------- INIT ---------
setup_tracing()

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("eu-gateway")

app = FastAPI(title="EU Health Gateway")
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

# --------- API ---------
@app.post("/exchange")
def exchange(data: dict):
    logger.info({
        "service": "eu-gateway",
        "event": "forwarding_request",
        "department": data["department"],
        "exam": data["exam"]
    })

    time.sleep(0.2)

    response = requests.post(
        "http://de-registry:8000/records",
        json=data,
        timeout=5
    )

    return response.json()
