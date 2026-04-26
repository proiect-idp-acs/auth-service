from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
import datetime
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="PlayerAuth Service", description="Gestionează autentificarea și JWT")

# Secret key pentru a semna token-urile jwt
SECRET_KEY = "super_secret_tennis_key"

# Schema pentru datele primite de la utilizator
class LoginRequest(BaseModel):
    username: str
    password: str

# Activam instrumentarea pentru monitorizare cu Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"message": "PlayerAuth Service este activ"}

@app.post("/api/auth/login")
def login(request: LoginRequest):
    # Test user pentru arbitru
    if request.username == "arbitru1" and request.password == "parola123":
        # Generam token-ul JWT valabil 1h
        payload = {
            "sub": request.username,
            "role": "arbitru",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Credențiale incorecte")

# TODO: Adauga ruta pentru validarea token-ului JWT și extragerea rolului utilizatorului