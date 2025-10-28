from fastapi import (FastAPI, Depends, HTTPException)
from sqlalchemy.orm import Session
from schemas.petHost import PetHostSchema, PetPreferencesSchema, ServiceOfferSchema
from core.init import *
from core.database import *
from petHost.models import PetHost
from service.models import ServiceOffer
from petPreference.models import PetPreferences
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {
        "message":"Petbnb API"
    }

@app.get("/pet-host")
def petHost(db: Session = Depends(get_db)):
    hosts = db.query(PetHost).all()
    db.close()
    return hosts

@app.post("/pet-host")
def createPetHost(pethost:PetHostSchema):
    print(pethost)
    return pethost

@app.get("/pet-host/pet-preference/{petHostId}")
def getPetPreferenceForPetHost(
    petHostId: int, db: Session = Depends(get_db)):
    host = db.query(PetPreferences).filter(PetPreferences.pet_host_id == petHostId).first()
    return host

@app.post("/pet-host/pet-preference/{petHostId}")
def setPetPreferenceForPetHost(petHostId: int, petPreference: PetPreferencesSchema):
    print("petHostId")
    return petPreference

@app.post("/pet-host/service/{petHostId}")
def setServiceOfferForPetHost(petHostId:int, service:ServiceOfferSchema):
    return service

@app.get("/pet-host/service/{petHostId}")
def getServiceOfferForPetHost(petHostId:int, db: Session = Depends(get_db)):
    service = db.query(ServiceOffer).filter(ServiceOffer.pet_host_id==petHostId).first()
    return service


@app.post("/pet-host/image-gallery")
def setImageGalleryForPetHost():
    pass

@app.post("/pet-host/certification")
def setCertificationForPetHost():
    pass

@app.get("/pet-host/{hostId}")
def get_pet_host(hostId: int, db: Session = Depends(get_db)):
    host = db.query(PetHost).filter(PetHost.id == hostId).first()
    if not host:
        raise HTTPException(status_code=404, detail="PetHost not found")
    return host