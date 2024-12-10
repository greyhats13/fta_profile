# Path: fta_profile/app/infrastructure/logger.py

import sys, logging, ujson
from datetime import datetime
from aiologger import Logger as AsyncLogger
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.formatters.base import Formatter
from google.cloud.logging_v2.handlers import CloudLoggingFilter
from ..adapter.middleware import http_request_context


class JSONFormatter(Formatter):
    def __init__(self, project_id):
        self.project_id = project_id

    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": record.levelname,
            "http_request": http_request_context.get(),
        }
        print(
            f"otelTraceID: {record.otelTraceID}, otelSpanID: {record.otelSpanID}s, otelTraceSampled: {record.otelTraceSampled}"
        )
        log_record["trace"] = (
            f"projects/{self.project_id}/traces/{record.otelTraceID}" if record.OtelTraceID else None
        )
        log_record["span_id"] = record.otelSpanID if record.otelSpanID else None
        log_record["trace_sampled"] = record.otelTraceSampled if record.otelTraceSampled else None
        if hasattr(record, "msg"):
            log_record["msg"] = record.msg
        print(f"record:{record} ")
        return ujson.dumps(log_record)


class Logger:
    def __init__(self, app):
        # logging.getLogger("uvicorn.error").handlers = [logging.NullHandler()]
        # logging.getLogger("uvicorn.access").handlers = [logging.NullHandler()]
        # logging.getLogger("uvicorn").handlers = [logging.NullHandler()]
        # logging.getLogger("asgi").handlers = [logging.NullHandler()]
        self.logger = AsyncLogger.with_default_handlers(
            name=app.state.settings.app_name
        )
        self.app = app
        self._setup_handlers()

    def _setup_handlers(self):
        # Hapus handler default jika ada
        if self.logger.handlers:
            self.logger.remove_handler(self.logger.handlers[0])
        # Tambahkan AsyncStreamHandler dengan JSONFormatter
        stream_handler = AsyncStreamHandler(
            stream=sys.stdout,
            formatter=JSONFormatter(self.app.state.settings.firestore_project_id),
        )
        self.logger.add_handler(stream_handler)
        # Disable log propagation
        self.logger.propagate = False

    async def shutdown(self):
        await self.logger.shutdown()


# class GoogleCloudLogFilter(CloudLoggingFilter):

#     def filter(self, record: logging.LogRecord) -> bool:
#         record.http_request = http_request_context.get()

#         # Filter out healthcheck logs
#         if record.http_request and '/v1/healthcheck' in record.http_request.get('requestUrl', ''):
#             return False  # Skip logging this record

#         trace = cloud_trace_context.get()
#         split_header = trace.split('/', 1)

#         # Safely extract trace ID
#         if len(split_header) > 0:
#             trace_id = split_header[0]
#             if trace_id:
#                 record.trace = f"projects/{self.project}/traces/{trace_id}"
#                 # Safely extract span ID and trace_sampled
#                 if len(split_header) > 1:
#                     header_suffix = split_header[1]
#                     record.span_id = re.findall(r'^\w+', header_suffix)[0]
#                     record.trace_sampled = True
#         super().filter(record)
#         return True

# class GoogleCloudLogFilter(CloudLoggingFilter):

#     def filter(self, record: logging.LogRecord) -> bool:
#         record.http_request = http_request_context.get()
#         # Filter out healthcheck logs
#         if record.http_request and '/v1/healthcheck' in record.http_request.get('requestUrl', ''):
#             return False  # Skip logging this record
#         # Get OpenTelemetry's current span
#         span = trace.get_current_span()
#         span_context = span.get_span_context()

#         # Get the trace ID and span ID
#         trace_id = format(span_context.trace_id, '032x')
#         span_id = format(span_context.span_id, '016x')

#         if span_context.trace_id != 0:
#             record.trace = f"projects/{self.project}/traces/{trace_id}"
#             record.span_id = span_id
#             record.trace_sampled = span_context.trace_flags.sampled

#         # Set http_request if available
#         record.http_request = getattr(record, 'http_request', None)

#         super().filter(record)
#         return True
