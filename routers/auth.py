from fastapi import APIRouter, HTTPException

from models.user_model import User
from database.mongodb import user_collection
from auth.hash import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(user: User):

    existing_user = user_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(
            user.password
        )
    }

    result = user_collection.insert_one(
        user_data
    )

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }





from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth.hash import verify_password
from auth.jwt_handler import create_access_token
from database.mongodb import user_collection


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = user_collection.find_one(
        {"email": form_data.username}
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
        form_data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token({
        "sub": user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/me")
def get_me(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, "mysecretkey", algorithms=["HS256"])
        return {
            "email": payload.get("sub")
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )