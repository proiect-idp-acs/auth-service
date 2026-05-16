from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
import datetime
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PlayerAuth Service", description="Gestionează autentificarea și JWT (RBAC)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Instrumentator().instrument(app).expose(app)

SECRET_KEY = "super_secret_tennis_key"

class LoginRequest(BaseModel):
    username: str
    password: str

# Baza de date pentru utilizatori și rolurile lor
USERS_DB = {
    "arbitru1": {"password": "parola123", "role": "arbitru"},
    "spectator1": {"password": "parola123", "role": "spectator"}
}

@app.get("/")
def read_root():
    return {"message": "PlayerAuth Service este activ!"}

@app.post("/api/auth/login")
def login(request: LoginRequest):
    user = USERS_DB.get(request.username)
    
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Credențiale incorecte")
        
    # Generam token-ul
    payload = {
        "sub": request.username,
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}