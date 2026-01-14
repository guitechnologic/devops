from fastapi import FastAPI
import random
import time
import logging

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("de-registry")

app = FastAPI(title="DE Health Registry")
FastAPIInstrumentor.instrument_app(app)

@app.post("/records")
def records(data: dict):
    processing_time = random.uniform(0.5, 2.0)
    time.sleep(processing_time)

    logger.info({
        "service": "de-registry",
        "event": "exam_processed",
        "department": data["department"],
        "exam": data["exam"],
        "latency_ms": int(processing_time * 1000)
    })

    return {
        "status": "completed",
        "exam": data["exam"],
        "department": data["department"],
        "performed_at": "Berlin",
        "latency_ms": int(processing_time * 1000)
    }
