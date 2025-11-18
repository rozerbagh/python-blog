import time
from fastapi import Request


# --------------------------
# 1️⃣ Logging Middleware
# --------------------------
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"[LOG] {request.method} {request.url.path} - {duration:.2f}s")
    return response