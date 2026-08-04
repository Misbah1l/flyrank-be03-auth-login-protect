from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase_client import supabase


app = FastAPI(
    title="BE-03 Auth API",
    version="1.0.0"
)
security = HTTPBearer()

class UserAuth(BaseModel):
    email: str
    password: str

@app.get("/")
def home():
    return {
        "message": "Server running and connected to Supabase"
    }
@app.post("/auth/signup", status_code=201)
def signup(user: UserAuth):

    if not user.email or not user.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": user.email,
                "password": user.password,
            }
        )

        return {
            "message": "User created successfully",
            "user": response.user
        }

    except Exception as e:
        print("SIGNUP ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/auth/login")
def login(user: UserAuth):

    if not user.email or not user.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": user.email,
                "password": user.password,
            }
        )

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )
@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }
@app.get("/protected/profile")
def protected_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)

        return {
            "id": response.user.id,
            "email": response.user.email,
            "created_at": response.user.created_at
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )