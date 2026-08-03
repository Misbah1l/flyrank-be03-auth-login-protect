from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from supabase_client import supabase


app = FastAPI(
    title="BE-03 Auth API",
    version="1.0.0"
)

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
def protected_profile(authorization: str = Header(None)):

    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    token = authorization.replace("Bearer ", "")

    return {
        "message": "Token received successfully",
        "token": token
    }