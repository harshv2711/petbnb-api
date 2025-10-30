from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.init import *
from schemas.petHost import *

router = APIRouter(prefix="/booking")

@router.get("/")
def bookingHome():
    return {
        "message": "booking home"
    }