from fastapi import FastAPI, Depends, HTTPException
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from database import SessionLocal, Base, engine
from models import Client
from rbac import check_role

load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="MSP vCIO Platform API")

# Load Auth0 credentials from environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

# OAuth setup for Auth0
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    authorize_url=f"https://{AUTH0_DOMAIN}/authorize",
    access_token_url=f"https://{AUTH0_DOMAIN}/oauth/token",
    client_kwargs={"scope": "openid profile email"},
)

# Initialize database
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### 🔹 HOME ROUTE ###
@app.get("/")
def home():
    return {"message": "MSP vCIO platform is running!"}

### 🔹 AUTHENTICATION ROUTES ###
@app.get("/login")
async def login(request: Request):
    """Redirects the user to Auth0 for authentication."""
    try:
        return await oauth.auth0.authorize_redirect(request, AUTH0_CALLBACK_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth0 login failed: {str(e)}")

@app.get("/auth/callback")
async def auth_callback(request: Request):
    """Handles Auth0 callback and extracts user information."""
    try:
        token = await oauth.auth0.authorize_access_token(request)
        user = await oauth.auth0.parse_id_token(request, token)

        if not user:
            raise HTTPException(status_code=400, detail="Authentication failed")

        # Extract roles from Auth0 custom claims
        roles = user.get("https://dev-y21yym5fgf78ufvb.us.auth0.com/roles", [])
        
        return {"user": user, "roles": roles}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth0 callback error: {str(e)}")

### 🔹 CLIENT MANAGEMENT ROUTES ###
@app.post("/clients/")
def create_client(name: str, email: str, db: Session = Depends(get_db)):
    """Creates a new client record."""
    new_client = Client(name=name, email=email)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@app.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    """Retrieves all clients."""
    return db.query(Client).all()

### 🔹 ROLE-BASED ACCESS CONTROL ROUTES ###
@app.get("/admin-data/")
def admin_data(request: Request, allowed: bool = Depends(check_role(["MSP Admin"]))):
    """Restricted data for MSP Admins."""
    return {"message": "This is sensitive admin data"}

@app.get("/vcio-data/")
def vcio_data(request: Request, allowed: bool = Depends(check_role(["vCIO"]))):
    """Restricted data for vCIOs."""
    return {"message": "This is vCIO-specific data"}

@app.get("/vciso-data/")
def vciso_data(request: Request, allowed: bool = Depends(check_role(["vCISO"]))):
    """Restricted data for vCISOs."""
    return {"message": "This is vCISO-specific security data"}

@app.get("/client-data/")
def client_data(request: Request, allowed: bool = Depends(check_role(["Client"]))):
    """Restricted data for clients."""
    return {"message": "Client-specific data"}
