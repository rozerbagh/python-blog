from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt
from datetime import timedelta

from starlette.config import undefined

from db import get_db
from models import UserModel, UserBaseModel
from utils.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Fetch user by email (username field holds email in this case)
    result = await db.execute(select(UserModel).where(UserModel.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create JWT token
    access_token = create_access_token(data={"sub": user.email, "id": user.id, "phone": user.phone})
    return {
        "message": "Logged In Successfully",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email,
            "phone": user.phone
        }
    }


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # fetch user from DB
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user


@router.post("/register")
async def create_user(user: UserBaseModel, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(UserModel).where(UserModel.email == user.email))
        exist_user = result.scalar_one_or_none()
        if exist_user:
            return JSONResponse(status_code=status.HTTP_302_FOUND, content={"message": "User already exists", "data": undefined})
        new_user = UserModel(fullname=user.fullname, password=user.password, email=user.email, phone=user.phone)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created", "data": new_user})

    # except IntegrityError:
    #     # Example: unique constraint violation (duplicate email)
    #     await db.rollback()
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="User with this email already exists"
    #     )
    #
    # except SQLAlchemyError as e:
    #     # Catch all other SQL errors
    #     await db.rollback()
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Database error: {str(e)}"
    #     )
    except Exception as e:
        print(e)
        # Any unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )