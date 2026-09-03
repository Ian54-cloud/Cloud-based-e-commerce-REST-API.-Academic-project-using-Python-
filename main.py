import time
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

# CONFIGURATION SETUP
SECRET_KEY = "grade-4-assignment-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# CONFIGURE LOGGING
logging.basicConfig(
    filename='api_access.log', 
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

app = FastAPI(title="Cloud E-commerce REST API")

# DATABASE MODELS
class Product(BaseModel):
    id: int
    name: str
    price: float

class Order(BaseModel):
    product_id: int
    quantity: int

class Token(BaseModel):
    access_token: str
    token_type: str

# MIDDLEWARE
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        log_message = f"Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | Duration: {process_time:.4f}s"
        logging.info(log_message)
        print(log_message) # So you can see it in the CodeSandbox console
        return response

app.add_middleware(LoggingMiddleware)

# BUSINESS LOGIC
class ProductService:
    def __init__(self):
        self.db = [
            {"id": 1, "name": "Laptop", "price": 999.99},
            {"id": 2, "name": "Cloud Subscription", "price": 49.99}
        ]

    def get_all(self):
        return self.db

    def find_by_id(self, p_id: int):
        return next((p for p in self.db if p["id"] == p_id), None)

product_service = ProductService()

#AUTHENTICATION(SECURITY)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

#CONTROLLERS

@app.get("/")
def health_check():
    return {"status": "online", "cloud_ready": True}

@app.get("/products", response_model=List[Product])
def get_products():
    """Public catalog access"""
    return product_service.get_all()

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Secure login to get JWT"""
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: Order, current_user: str = Depends(get_current_user)):
    """Protected resource - requires login"""
    product = product_service.find_by_id(order.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "user": current_user,
        "message": "Order placed successfully",
        "total": product["price"] * order.quantity
    }
