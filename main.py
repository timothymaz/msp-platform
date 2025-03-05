from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from database import SessionLocal, Base, engine
from models import Client
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# ✅ Add SessionMiddleware (Required for Auth0)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "supersecretkey"))

# ✅ Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    authorize_url=f"https://{AUTH0_DOMAIN}/authorize",
    access_token_url=f"https://{AUTH0_DOMAIN}/oauth/token",
    client_kwargs={"scope": "openid profile email"},
)

# ✅ Database Setup
Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get the database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Pydantic Model for Clients
class ClientCreate(BaseModel):
    name: str
    email: str

class ClientResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# ✅ Auth0 Login Route
@app.get("/login")
async def login(request: Request):
    """Redirects the user to Auth0 for authentication."""
    return await oauth.auth0.authorize_redirect(request, AUTH0_CALLBACK_URL)

# ✅ Auth0 Callback Route
@app.get("/auth/callback")
async def auth_callback(request: Request):
    """Handles Auth0 callback and extracts user information."""
    token = await oauth.auth0.authorize_access_token(request)
    user = await oauth.auth0.parse_id_token(request, token)

    if not user:
        raise HTTPException(status_code=400, detail="Authentication failed")

    return {"user": user}

# ✅ API Endpoints

@app.get("/")
def home():
    return {"message": "Welcome to the MSP vCIO Platform API"}

# ✅ Clients API
@app.post("/clients/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Create a new client."""
    db_client = Client(name=client.name, email=client.email)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    """Retrieve all clients."""
    return db.query(Client).all()

# ✅ Admin API
@app.get("/admin-data/")
def get_admin_data():
    return {"message": "Admin data here"}

# ✅ vCIO API
@app.get("/vcio-data/")
def get_vcio_data():
    return {"message": "vCIO data here"}

# ✅ vCISO API
@app.get("/vciso-data/")
def get_vciso_data():
    return {"message": "vCISO data here"}

# ✅ Client API
@app.get("/client-data/")
def get_client_data():
    return {"message": "Client data here"}
