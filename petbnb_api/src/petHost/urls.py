from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.init import *
from schemas.petHost import *

router = APIRouter(prefix="")

@router.get("/filter")
def filterHost(db: Session = Depends(get_db)):
    hosts = db.query(PetHost).all()
    db.close()
    return hosts

@router.get("/")
def home():
    return {
        "message":"Petbnb API"
    }

@router.get("/pet-host")
def petHost(db: Session = Depends(get_db)):
    hosts = db.query(PetHost).all()
    db.close()
    return hosts

@router.post("/pet-host")
def createPetHost(pethost:PetHostSchema):
    print(pethost)
    return pethost

@router.get("/pet-host/pet-preference/{petHostId}")
def getPetPreferenceForPetHost(
    petHostId: int, db: Session = Depends(get_db)):
    host = db.query(PetPreferences).filter(PetPreferences.pet_host_id == petHostId).first()
    return host

@router.post("/pet-host/pet-preference/{petHostId}")
def setPetPreferenceForPetHost(petHostId: int, petPreference: PetPreferencesSchema):
    print("petHostId")
    return petPreference

@router.post("/pet-host/service/{petHostId}")
def setServiceOfferForPetHost(petHostId:int, service:ServiceOfferSchema):
    return service

@router.get("/pet-host/service/{petHostId}")
def getServiceOfferForPetHost(petHostId:int, db: Session = Depends(get_db)):
    service = db.query(ServiceOffer).filter(ServiceOffer.pet_host_id==petHostId).first()
    return service


@router.post("/pet-host/image-gallery")
def setImageGalleryForPetHost():
    pass

@router.post("/pet-host/certification")
def setCertificationForPetHost():
    pass

@router.get("/pet-host/{hostId}")
def get_pet_host(hostId: int, db: Session = Depends(get_db)):
    host = db.query(PetHost).filter(PetHost.id == hostId).first()
    if not host:
        raise HTTPException(status_code=404, detail="PetHost not found")
    return host