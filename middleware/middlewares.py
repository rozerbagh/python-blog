import time
from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from utils.security import SECRET_KEY, ALGORITHM

# --------------------------
# 1️⃣ Logging Middleware
# --------------------------
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"[LOG] {request.method} {request.url.path} - {duration:.2f}s")
    return response


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


# --------------------------
# 3️⃣ Optional JWT Validator
# --------------------------
async def verify_jwt_middleware(request: Request, call_next):
    if request.url.path.startswith(("/auth", "/docs", "/openapi")):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"message": "Missing or invalid token"})

    token = auth_header.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return JSONResponse(status_code=401, content={"message": "Invalid or expired token"})

    return await call_next(request)