from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Field
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



# ---------- Pydantic Schemas ----------

class PetHostUpdate(BaseModel):
    # Only include fields you want to allow updating (all optional for PATCH).
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None
    bio: Optional[str] = None
    experience: Optional[str] = None
    address: Optional[str] = None
    account_status: Optional[str] = Field(default=None, description="e.g., under_review | active | suspended")
    rating: Optional[float] = None
    profile_image: Optional[str] = None
    is_verified: Optional[bool] = None
    number_of_pet_hosted: Optional[int] = None
    hosting_capacity: Optional[int] = None
    language: Optional[str] = None
    availability_status: Optional[str] = Field(default=None, description="e.g., available | busy | away")
    is_superhost: Optional[bool] = None
    total_review: Optional[int] = None
    total_earnings: Optional[float] = None

    class Config:
        extra = "forbid"  # reject unexpected fields


class PetHostOut(BaseModel):
    id: int
    user_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    mobile_number: Optional[str]
    bio: Optional[str]
    experience: Optional[str]
    address: Optional[str]
    account_status: Optional[str]
    rating: float
    profile_image: Optional[str]
    is_verified: bool
    number_of_pet_hosted: int
    hosting_capacity: int
    language: Optional[str]
    availability_status: Optional[str]
    is_superhost: bool
    total_review: int
    total_earnings: float

    class Config:
        from_attributes = True  # Pydantic v2; for v1 use orm_mode = True


# ---------- Endpoint: Partial Update (PATCH) ----------

@router.patch("/pet-host/{host_id}", response_model=PetHostOut, status_code=status.HTTP_200_OK)
def update_pet_host(
    host_id: int,
    payload: PetHostUpdate,
    db: Session = Depends(get_db),
):
    # Fetch
    host: PetHost | None = db.query(PetHost).filter(PetHost.id == host_id).first()
    if not host:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PetHost not found")

    # Fields you will never allow to be updated via this endpoint
    IMMUTABLE_FIELDS = {"id", "user_id", "created_at", "updated_at"}

    # Apply only provided fields
    update_data = payload.model_dump(exclude_unset=True)

    # Optionally: lightweight guardrails/normalization
    if "rating" in update_data and update_data["rating"] is not None:
        r = update_data["rating"]
        if r < 0 or r > 5:
            raise HTTPException(status_code=422, detail="rating must be between 0 and 5")

    for field, value in update_data.items():
        if field in IMMUTABLE_FIELDS:
            continue
        setattr(host, field, value)

    # Commit
    try:
        db.add(host)
        db.commit()
        db.refresh(host)
    except Exception as e:
        db.rollback()
        # You can branch on IntegrityError for unique constraints, etc.
        raise HTTPException(status_code=400, detail=f"Update failed: {e.__class__.__name__}")

    return host
