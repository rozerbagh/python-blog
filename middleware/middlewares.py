from fastapi import Request
from fastapi.responses import JSONResponse
from middleware import log_requests, verify_jwt_middleware


# --------------------------
# 2️⃣ Global Error Handler
# --------------------------
async def global_exception_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(f"[ERROR] {request.method} {request.url.path}: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal Server Error",
                "error": str(e)
            },
        )


def register_middlewares(app):
    app.middleware("http")(log_requests)
    app.middleware("http")(global_exception_handler)
    app.middleware("http")(verify_jwt_middleware)