from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.security import verify_password, create_access_token
from db.session import get_db
from models.user import User
from schemas.auth import LoginRequest, TokenResponse
from utils.response import build_response

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if user is None or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
        )

    token = create_access_token(user_id=user.id, role=user.role)
    result = TokenResponse(access_token=token)

    return build_response(
        status_code=status.HTTP_200_OK,
        data=result.model_dump(),
        message="Đăng nhập thành công",
    )
