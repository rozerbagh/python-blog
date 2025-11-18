from fastapi import APIRouter
from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserBaseModel, UserModel, UserListResponse, UserUpdateModel
from db.db import get_db
from routes.auth_routes import get_current_user
from utils.security import hash_password

# Create router instance
router = APIRouter(
    prefix="/users",  # URL prefix for all routes
    tags=["Users"],  # Tag for automatic docs grouping
)


@router.get("/", response_model=UserListResponse)
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "List of all users", "data": users})


@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()  # fetch single row or None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

        # Optionally, exclude sensitive info like password
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "id": user.id,
        "fullname": user.fullname,
        "email": user.email,
        "phone": user.phone
    })


@router.patch("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdateModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields dynamically
    update_data = user_update.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "message": "User updated successfully",
        "data": {
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email,
            "phone": user.phone,
        }
    })

