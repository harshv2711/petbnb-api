from fastapi import (FastAPI)
from core.init import *
from core.database import *
Base.metadata.create_all(bind=engine)
from routers import petHostRouter, bookingRouter, petPreferenceRouter
app = FastAPI()

app.include_router(petHostRouter) # petHost app urls
app.include_router(bookingRouter) # booking app urls
app.include_router(petPreferenceRouter) # booking app urls

@app.get("/")
def home():
    return {
        "message":"Petbnb API" }