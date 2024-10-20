from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.or import Session
# from common.database import SessionLocal
# from project1 import models, schemas

router = APIRouter()

@router.get("/")
async def get_status():
    return {"status": "personal Website router status - OK"}


