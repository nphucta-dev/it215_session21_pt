# Secure Login API

## Cài đặt
```bash
pip install -r requirements.txt
```

## Cấu hình
File `.env` đã có sẵn `JWT_SECRET_KEY` sinh ngẫu nhiên (32 bytes) và `DATABASE_URL` mẫu.
Sửa `DATABASE_URL` cho đúng MySQL của bạn.

**Lưu ý:** không commit file `.env` lên Git. Thêm `.env` vào `.gitignore`.

## Chạy
```bash
uvicorn main:app --reload
```
(cần thêm file `main.py` include router `auth_router` vào app FastAPI của bạn)

## Cấu trúc
```
secure_login/
├── core/security.py      # hash password, tạo/giải mã JWT
├── db/
│   ├── base.py            # Declarative Base
│   └── session.py         # engine, get_db()
├── models/user.py         # User model (password lưu bcrypt hash)
├── schemas/auth.py        # LoginRequest, TokenResponse
├── routers/auth_router.py # POST /auth/login
├── utils/response.py      # build_response()
├── .env                   # secret key + db url
└── requirements.txt
```
