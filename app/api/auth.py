from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.user import User
from app.core.security import (
    hash_password,
    create_access_token,
    create_refresh_token
)
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest
)
from app.services.auth_service import (
    authenticate_user,
    rotate_refresh_token
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role="user",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(
            {"sub": str(user.id), "role": user.role}
        ),
        refresh_token=create_refresh_token(
            {"sub": str(user.id)}
        ),
        token_type="bearer"
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return TokenResponse(
        access_token=create_access_token(
            {"sub": str(user.id), "role": user.role,"email": user.email}
        ),
        refresh_token=create_refresh_token(
            {"sub": str(user.id)}
        ),
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest, db: Session = Depends(get_db)):

    try:
        new_refresh, user_id = rotate_refresh_token(db, request.refresh_token)

        return TokenResponse(
            access_token=create_access_token({"sub": str(user_id)}),
            refresh_token=new_refresh,
            token_type="bearer"
        )

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")