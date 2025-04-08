from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok", 
        "message": f"{settings.PROJECT_NAME} is running",
        "version": settings.VERSION
    } 