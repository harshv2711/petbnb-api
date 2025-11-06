from fastapi import APIRouter, Depends
from pydantic import BaseModel, HttpUrl
from core.database import get_db
from sqlalchemy.orm import Session
from .models import PetProfile

router = APIRouter(prefix="/pet-profile", tags=["Pet Profile"])

class PetProfileFormDataInputSchema(BaseModel):
    user_id: str
    pet_name: str
    pet_type: str
    breed: str
    gender: str
    is_vaccinated: bool
    is_friendly_with_children: bool
    pet_profile_image_url: str  # corrected from bool → URL


@router.post("/")
def create(petProfileFormData:PetProfileFormDataInputSchema, db:Session = Depends(get_db)):
    
    existingPetProfile = (
    db.query(PetProfile)
    .filter(PetProfile.pet_name == petProfileFormData.pet_name)
    .filter(PetProfile.user_id == petProfileFormData.user_id)  # optional: avoid duplicates per user
    .first()
    )

    if existingPetProfile:
        return {
            "error": True,
            "message": "Profile already exists"
        }
    else:
        newPetProfile = PetProfile(
            user_id=petProfileFormData.user_id,
            pet_name=petProfileFormData.pet_name,
            pet_type=petProfileFormData.pet_type,
            breed=petProfileFormData.breed,
            gender=petProfileFormData.gender,
            is_vaccinated=petProfileFormData.is_vaccinated,
            is_friendly_with_children=petProfileFormData.is_friendly_with_children,
            pet_profile_image_url=petProfileFormData.pet_profile_image_url
        )

        db.add(newPetProfile)
        db.commit()
        db.refresh(newPetProfile)
        return newPetProfile