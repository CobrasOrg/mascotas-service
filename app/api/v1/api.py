from fastapi import APIRouter
from app.api.v1.endpoints import base

api_router = APIRouter()

# Import and include other routers here
# Example:
# from app.api.v1.endpoints import users, items
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])

api_router.include_router(base.router, prefix="/base", tags=["base"]) 