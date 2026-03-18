import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        started_at = time.perf_counter()
        request.state.request_id = str(uuid.uuid4())

        response = await call_next(request)

        process_time = time.perf_counter() - started_at
        request.state.process_time = process_time

        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        response.headers["X-Request-ID"] = request.state.request_id

        return response