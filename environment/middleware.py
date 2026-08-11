import time
import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

# Paths we want to measure (exact match)
MEASURED_PATHS = {
    "/",
    "/analytics/",
    "/countries/",
    "/reports/",
    "/map/",
}


class PerfTimingMiddleware(MiddlewareMixin):
    """Log a single line with total request duration for selected paths."""

    def process_request(self, request):
        # store start time on the request object
        request._perf_start = time.perf_counter()

    def process_response(self, request, response):
        start = getattr(request, "_perf_start", None)
        if start is not None and request.path in MEASURED_PATHS:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "PERF path=%s status=%s duration_ms=%.2f",
                request.path,
                response.status_code,
                duration_ms,
            )
        return response