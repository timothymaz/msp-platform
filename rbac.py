from fastapi import HTTPException, Depends
from starlette.requests import Request

def check_role(required_roles: list):
    def role_checker(request: Request):
        user_roles = request.state.user.get("roles", [])
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(status_code=403, detail="Access denied")
        return True
    return role_checker
