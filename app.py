from fastapi import FastAPI, Depends, HTTPException
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

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

@app.get("/login")
async def login(request: Request):
    return await oauth.auth0.authorize_redirect(request, AUTH0_CALLBACK_URL)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    user = await oauth.auth0.parse_id_token(request, token)

    if not user:
        raise HTTPException(status_code=400, detail="Authentication failed")

    # Extract roles from Auth0
    roles = user.get("https://dev-y21yym5fgf78ufvb.us.auth0.com/roles", [])  # Auth0 stores roles in custom claims

    return {"user": user, "roles": roles}
