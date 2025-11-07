from fastapi import APIRouter, Depends, HTTPException
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

class UpdatePetProfileFormDataInputSchema(BaseModel):
    user_id: str
    id: int
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
    
@router.put("/")
def update_pet_profile(petProfileFormData: UpdatePetProfileFormDataInputSchema, db: Session = Depends(get_db)):
    # Check if the profile exists
    existingPetProfile = (
        db.query(PetProfile)
        .filter(PetProfile.id == petProfileFormData.id)  # identify by unique ID
        .filter(PetProfile.user_id == petProfileFormData.user_id)
        .first()
    )

    if not existingPetProfile:
        raise HTTPException(status_code=404, detail="Pet profile not found")

    # Update fields
    existingPetProfile.pet_name = petProfileFormData.pet_name
    existingPetProfile.pet_type = petProfileFormData.pet_type
    existingPetProfile.breed = petProfileFormData.breed
    existingPetProfile.gender = petProfileFormData.gender
    existingPetProfile.is_vaccinated = petProfileFormData.is_vaccinated
    existingPetProfile.is_friendly_with_children = petProfileFormData.is_friendly_with_children
    existingPetProfile.pet_profile_image_url = petProfileFormData.pet_profile_image_url

    db.commit()
    db.refresh(existingPetProfile)

    return {
        "error": False,
        "message": "Pet profile updated successfully",
        "data": existingPetProfile
    }

    
@router.get("/{user_id}/{pet_profile_id}")
def getOnePetProfileBasedOnUser(user_id: str, pet_profile_id: int, db:Session = Depends(get_db)):
    petProfile = (
        db.query(PetProfile)
        .filter(PetProfile.id == pet_profile_id)
        .filter(PetProfile.user_id == user_id)  # optional: avoid duplicates per user
        .first()
    )

    return petProfile

@router.get("/{user_id}")
def getAllPetProfileBasedOnUser(user_id: str, db:Session = Depends(get_db)):
    petProfileList = (
        db.query(PetProfile)
        .filter(PetProfile.user_id == user_id)  # optional: avoid duplicates per user
        .all()
    )

    return petProfileList