from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.database import get_database

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"} 