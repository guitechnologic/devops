from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import os

def setup_tracing():
    resource = Resource.create({
        "service.name": os.getenv("OTEL_SERVICE_NAME", "unknown"),
        "service.namespace": "eu-health",
        "deployment.environment": "lab",
    })

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
        insecure=True,
    )

    provider.add_span_processor(BatchSpanProcessor(exporter))
