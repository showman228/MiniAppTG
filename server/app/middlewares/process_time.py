from typing import Callable, Awaitable
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        end_time = time.perf_counter()
        process_time = end_time - start_time
        response.headers["X-Process-Time"] = f"{process_time:.5f}"
        return response
