from fastapi import APIRouter, Depends, HTTPException
from core.init import *
from core.database import get_db
from sqlalchemy.orm import Session
from .schemas import CreatePetPreferenceInputSchema
from core.init import PetPreferences, PetHost

router = APIRouter(prefix="/pet-preference")

@router.post('/')
def setPetPreference(
    petPreferenceData: CreatePetPreferenceInputSchema,
    db: Session = Depends(get_db)):
    # Check if host exists
    existingHost = db.query(PetHost).filter(PetHost.user_id == petPreferenceData.user_id).first()
    if not existingHost:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Host account does not exist"
            }
        )

    # Check if pet preferences already exist for this host
    existingPreference = db.query(PetPreferences).filter(PetPreferences.pet_host_id == existingHost.id).first()

    # If it exists, update it
    if existingPreference:
        existingPreference.pet_type = petPreferenceData.pet_type
        existingPreference.pet_size_accepted = petPreferenceData.pet_size_accepted
        existingPreference.age_range = petPreferenceData.age_range
        existingPreference.special_needs_pet_accepted = petPreferenceData.special_needs_pet_accepted
        existingPreference.medical_needs_pet_accepted = petPreferenceData.medical_needs_pet_accepted
        db.commit()
        db.refresh(existingPreference)
        return {
            "error": False,
            "message": "Pet preferences updated successfully",
            "data": existingPreference
        }

    # Otherwise, create new preferences
    newPreference = PetPreferences(
        pet_host_id=existingHost.id,
        pet_type=petPreferenceData.pet_type,
        pet_size_accepted=petPreferenceData.pet_size_accepted,
        age_range=petPreferenceData.age_range,
        special_needs_pet_accepted=petPreferenceData.special_needs_pet_accepted,
        medical_needs_pet_accepted=petPreferenceData.medical_needs_pet_accepted
    )
    db.add(newPreference)
    db.commit()
    db.refresh(newPreference)

    return {
        "message": "Pet preferences created successfully",
        "data": newPreference
    }

