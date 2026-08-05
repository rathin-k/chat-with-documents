from fastapi import APIRouter, HTTPException, status

from app.models.user import UserSignup, UserLogin
from app.services.auth_service import create_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED
)
def signup(user: UserSignup):

    user_id = create_user(user)

    if user_id is None:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail="Email already registered"
      )

    return {
    "message": "User created successfully",
    "user_id": user_id
    }


@router.post("/login")
def login(user: UserLogin):

    token = login_user(user)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return token