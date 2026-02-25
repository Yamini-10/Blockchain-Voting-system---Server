from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.refresh_token import RefreshToken
from app.core.security import create_refresh_token
from app.core.config import settings
from app.models.user import User
from app.core.security import verify_password

def create_and_store_refresh_token(db: Session, user_id: int):
    token = create_refresh_token()
    expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    db_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires
    )

    db.add(db_token)
    db.commit()
    return token


def verify_refresh_token(db: Session, token: str):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if not db_token:
        raise Exception("Invalid refresh token")

    if db_token.expires_at < datetime.utcnow():
        raise Exception("Refresh token expired")

    return db_token


def rotate_refresh_token(db: Session, old_token: str):
    db_token = verify_refresh_token(db, old_token)

    user_id = db_token.user_id

    db.delete(db_token)
    db.commit()

    return create_and_store_refresh_token(db, user_id), user_id

def authenticate_user(db: Session, email: str, password: str):
   
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user