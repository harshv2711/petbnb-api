from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from core.database import get_db
from core.init import PetProfile as PetProfileModel, PetImage

router = APIRouter(prefix="/pet-profile", tags=["Pet Profile"])


# ---------------- Pydantic Schemas ----------------
class PetProfileBase(BaseModel):
    pet_name: str = Field(..., example="Buro")
    pet_type: Optional[str] = Field(None, example="Dog")
    pet_age: Optional[str] = Field(None, example="5 Years")
    breed: Optional[str] = Field(None, example="Golden Retriever")
    gender: Optional[str] = Field(None, example="Male")
    weight_kg: Optional[float] = Field(None, example=25.0)
    is_vaccinated: bool = Field(default=True)
    is_friendly_with_children: bool = Field(default=True)
    pet_profile_image_url: Optional[HttpUrl] = Field(None, example="https://example.com/pets/buro.jpg")


class PetProfileCreate(PetProfileBase):
    user_id: str = Field(..., example="USR_123")  # required once at creation


class PetProfileUpdate(PetProfileBase):
    pass


class PetProfileResponse(PetProfileBase):
    id: int
    user_id: str

    class Config:
        orm_mode = True


# ---------------- Endpoints ----------------

@router.post("/", response_model=PetProfileResponse, status_code=status.HTTP_201_CREATED)
def create_pet_profile(payload: PetProfileCreate, db: Session = Depends(get_db)):
    """Create a pet profile — one per user_id allowed."""
    existing = db.query(PetProfileModel).filter(PetProfileModel.user_id == payload.user_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {payload.user_id} already has a pet profile."
        )

    pet = PetProfileModel(
        user_id=payload.user_id,
        pet_name=payload.pet_name,
        pet_type=payload.pet_type,
        pet_age=payload.pet_age,
        breed=payload.breed,
        gender=payload.gender,
        weight_kg=payload.weight_kg,
        is_vaccinated=payload.is_vaccinated,
        is_friendly_with_children=payload.is_friendly_with_children,
        pet_profile_image_url=str(payload.pet_profile_image_url) if payload.pet_profile_image_url else None,
    )

    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("/{user_id}", response_model=PetProfileResponse)
def get_pet_profile(user_id: str, db: Session = Depends(get_db)):
    """Fetch a user's pet profile."""
    pet = db.query(PetProfileModel).filter(PetProfileModel.user_id == user_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet profile not found.")
    return pet


@router.patch("/{user_id}", response_model=PetProfileResponse)
def update_pet_profile(user_id: str, payload: PetProfileUpdate, db: Session = Depends(get_db)):
    """Update a user's pet profile."""
    pet = db.query(PetProfileModel).filter(PetProfileModel.user_id == user_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet profile not found.")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(pet, key, value)

    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet_profile(user_id: str, db: Session = Depends(get_db)):
    """Delete a user's pet profile."""
    pet = db.query(PetProfileModel).filter(PetProfileModel.user_id == user_id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet profile not found.")

    db.delete(pet)
    db.commit()
    return None
