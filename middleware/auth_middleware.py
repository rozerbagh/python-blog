from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError
from utils.security import SECRET_KEY, ALGORITHM
from models import UserModel
from db.db import get_db

# --------------------------
# 3️⃣ Optional JWT Validator
# --------------------------
async def verify_jwt_middleware(request: Request, call_next, db: AsyncSession = Depends(get_db)):
    if request.url.path.startswith(("/auth", "/docs", "/openapi")):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"message": "Missing or invalid token"})
    token = auth_header.split(" ")[1]
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        result = await db.execute(select(UserModel).where(UserModel.email == decode["email"]))
        user = result.scalar_one_or_none()
        request.state.user = user
    except JWTError:
        return JSONResponse(status_code=401, content={"message": "Invalid or expired token"})

    return await call_next(request)