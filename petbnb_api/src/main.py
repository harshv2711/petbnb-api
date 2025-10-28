from fastapi import (FastAPI, Depends, HTTPException)
from sqlalchemy.orm import Session
from schemas.petHost import PetHostSchema, PetPreferencesSchema, ServiceOfferSchema
from core.init import *
from core.database import *
Base.metadata.create_all(bind=engine)
from petHost.urls import router as pet_host_router

app = FastAPI()
app.include_router(pet_host_router)

@app.get("/")
def home():
    return {
        "message":"Petbnb API" }