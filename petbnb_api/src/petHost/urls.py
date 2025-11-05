from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.init import *
from schemas.petHost import *
from .schemas import CreateHostAccountInputSchema
from .models import PetHost

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
def createPetHost(hostData:CreateHostAccountInputSchema,  db: Session = Depends(get_db)):

    # 1. Check if a host already exists by user_id or email
    existing_host = db.query(PetHost).filter(
        (PetHost.user_id == hostData.user_id) | 
        (PetHost.email == hostData.email)
    ).first()

    if existing_host:
        # ✅ Return an API error response
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Host account already exists for this user.",
                # "existing_host_id": existing_host.id,
                # "email": existing_host.email
            }
        )

    #  2. Create a new host record if not found
    new_host = PetHost(
        user_id=hostData.user_id,
        first_name=hostData.first_name,
        last_name=hostData.last_name,
        email=hostData.email,
        mobile_number=hostData.mobile_number,
    )

    db.add(new_host)
    db.commit()
    db.refresh(new_host)

    return new_host


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