from fastapi import FastAPI

app = FastAPI(
    title="BE-03 Auth API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Server running and connected to Supabase"
    }