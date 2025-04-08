from fastapi import APIRouter

from app.api.routes import health, message
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(health.router, prefix="", tags=["health"])
api_router.include_router(message.router, prefix="/messages", tags=["messages"]) 