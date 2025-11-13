from fastapi import APIRouter
from fastapi import HTTPException, Depends, status
from typing import List
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserBaseModel, UserModel, UserListResponse
from db.db import get_db

# Create router instance
router = APIRouter(
    prefix="/users",  # URL prefix for all routes
    tags=["Users"],  # Tag for automatic docs grouping
)


@router.get("/",response_model=UserListResponse)
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"message": "List of all users","data": users}


@router.get("/{user_id}")
async def get_user(user_id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()  # fetch single row or None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

        # Optionally, exclude sensitive info like password
    return {
        "id": user.id,
        "fullname": user.fullname,
        "email": user.email,
        "phone": user.phone
    }


@router.post("/")
async def create_user(user: UserBaseModel ,db: AsyncSession = Depends(get_db)):
    try:
        new_user = UserModel(fullname=user.fullname, password=user.password, email=user.email, phone=user.phone)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"message": "User created", "data": new_user}

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
