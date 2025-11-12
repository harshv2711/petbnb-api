from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.database import get_db  # your SessionLocal dependency
# Import your models; adjust path if needed.
# If you already centralize models in core.init, keep using that.
from core.init import PetPreferences, PetHost

from .schemas import (
    PetPreferencesCreate,
    PetPreferencesUpdate,
    PetPreferencesOut,
)

router = APIRouter(prefix="/pet-preferences", tags=["Pet Preferences"])


# -------------------- Helpers --------------------

def _ensure_host_exists(db: Session, host_id: int):
    host = db.query(PetHost).filter(PetHost.id == host_id).first()
    if not host:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "message": "Host account does not exist"},
        )


def _get_by_id_or_404(db: Session, pref_id: int) -> PetPreferences:
    pref = db.query(PetPreferences).filter(PetPreferences.id == pref_id).first()
    if not pref:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "PetPreferences not found"},
        )
    return pref


# -------------------- CRUD --------------------

@router.post(
    "/",
    response_model=PetPreferencesOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create pet preferences (one per host)"
)
def create_pet_preferences(payload: PetPreferencesCreate, db: Session = Depends(get_db)):
    # Enforce one-to-one: each host can have only one preferences row
    _ensure_host_exists(db, payload.pet_host_id)

    existing = (
        db.query(PetPreferences)
        .filter(PetPreferences.pet_host_id == payload.pet_host_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": True, "message": "Preferences already exist for this host"},
        )

    pref = PetPreferences(
        pet_host_id=payload.pet_host_id,
        pet_type=payload.pet_type,
        pet_size_accepted=payload.pet_size_accepted,
        age_range=payload.age_range,
        special_needs_pet_accepted=payload.special_needs_pet_accepted,
        medical_needs_pet_accepted=payload.medical_needs_pet_accepted,
    )
    db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref


@router.get(
    "/",
    response_model=List[PetPreferencesOut],
    summary="List pet preferences"
)
def list_pet_preferences(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    host_id: Optional[int] = Query(None, description="Filter by pet_host_id"),
):
    q = db.query(PetPreferences)
    if host_id is not None:
        q = q.filter(PetPreferences.pet_host_id == host_id)
    return q.offset(skip).limit(limit).all()


@router.get(
    "/{pref_id}",
    response_model=PetPreferencesOut,
    summary="Get pet preferences by ID"
)
def get_pet_preferences(pref_id: int, db: Session = Depends(get_db)):
    return _get_by_id_or_404(db, pref_id)


@router.get(
    "/by-host/{host_id}",
    response_model=PetPreferencesOut,
    summary="Get pet preferences by Host ID"
)
def get_pet_preferences_by_host(host_id: int, db: Session = Depends(get_db)):
    pref = (
        db.query(PetPreferences)
        .filter(PetPreferences.pet_host_id == host_id)
        .first()
    )
    if not pref:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "Preferences not found for this host"},
        )
    return pref


@router.patch(
    "/{pref_id}",
    response_model=PetPreferencesOut,
    summary="Update pet preferences (partial)"
)
def update_pet_preferences(
    pref_id: int,
    payload: PetPreferencesUpdate,
    db: Session = Depends(get_db),
):
    pref = _get_by_id_or_404(db, pref_id)

    # Apply only provided fields
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(pref, field, value)

    db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref


@router.put(
    "/upsert/by-host/{host_id}",
    response_model=PetPreferencesOut,
    summary="Upsert pet preferences by Host ID"
)
def upsert_pet_preferences_by_host(
    host_id: int,
    payload: PetPreferencesUpdate,
    db: Session = Depends(get_db),
):
    _ensure_host_exists(db, host_id)

    pref = (
        db.query(PetPreferences)
        .filter(PetPreferences.pet_host_id == host_id)
        .first()
    )

    if pref is None:
        pref = PetPreferences(pet_host_id=host_id)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(pref, field, value)

    db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref


@router.delete(
    "/{pref_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete pet preferences"
)
def delete_pet_preferences(pref_id: int, db: Session = Depends(get_db)):
    pref = _get_by_id_or_404(db, pref_id)
    db.delete(pref)
    db.commit()
    return None
