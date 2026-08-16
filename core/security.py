"""
1. Bảng phân tích vấn đề
#	Vấn đề	Nguy cơ	Cách khắc phục
1	Mật khẩu so sánh trực tiếp data.password != user.password	Mật khẩu đang lưu dạng plaintext trong DB — nếu DB bị lộ, toàn bộ mật khẩu người dùng bị lộ ngay lập tức	Băm mật khẩu bằng bcrypt (hoặc argon2) khi đăng ký, và dùng verify() để so sánh khi login
2	Secret key JWT hardcode "123456"	Secret yếu, dễ đoán, lộ trong source code (đặc biệt nếu push lên Git) → kẻ tấn công tự ký token giả với bất kỳ role nào (leo thang đặc quyền)	Lưu secret key trong biến môi trường (.env), dùng khóa đủ mạnh (≥32 bytes random), không commit vào repo
3	Payload JWT chứa password	Token chứa mật khẩu (dù đã hash) — token JWT chỉ được encode (Base64), không mã hóa, ai cũng decode đọc được nội dung	Payload chỉ nên chứa thông tin định danh cần thiết: sub (user id), role, không bao giờ chứa password
4	Không phân biệt lỗi "email không tồn tại" và "sai mật khẩu"	User enumeration attack — kẻ tấn công dò được email nào tồn tại trong hệ thống để tấn công có chủ đích (brute-force, phishing)	Trả về thông điệp chung: "Email hoặc mật khẩu không chính xác" cho cả hai trường hợp
5	JWT không có thời hạn (exp)	Token tồn tại vĩnh viễn, nếu bị đánh cắp thì kẻ tấn công dùng được mãi mãi, không thể thu hồi	Thêm claim exp (thời gian hết hạn, ví dụ 15-60 phút) và cân nhắc refresh token
6	Không giới hạn số lần đăng nhập sai (rate limiting)	Dễ bị brute-force dò mật khẩu	Thêm rate limiting theo IP/email (ví dụ slowapi) hoặc khóa tài khoản tạm thời sau N lần sai
7	Trả lỗi trực tiếp bằng dict thay vì HTTPException + status code	HTTP status luôn là 200 dù login thất bại → sai chuẩn REST, client khó xử lý logic, không đồng nhất với build_response()	Raise HTTPException(status_code=401, ...) để global exception handler xử lý và trả response chuẩn
"""

import os
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY chưa được cấu hình trong .env")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
