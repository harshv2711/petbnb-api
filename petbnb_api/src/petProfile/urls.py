from fastapi import APIRouter, Depends, status, HTTPException, Query, UploadFile, File
from .schema import PetProfileCreateSchema
from core.database import get_db
from sqlalchemy.orm import Session, joinedload
from core.init import PetProfile, PetPhotos
from .schema import PetAgeRangeEnum, PetGenderEnum, PetTypeEnum, PetProfileUpdateSchema
from typing import Optional, List
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/pet-profile", tags=["Pet Profile"])
# ---------- Helper ----------
def _get_pet_or_404(db: Session, pet_id: int) -> PetProfile:
    pet = db.query(PetProfile).filter(PetProfile.id == pet_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "Pet profile not found"},
        )
    return pet

def _save_image(file: UploadFile) -> str:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "message": "Only image files are allowed"},
        )

    ext = os.path.splitext(file.filename or "")[1] or ".jpg"
    file_id = uuid.uuid4().hex
    file_name = f"{file_id}{ext}"
    dest_path = MEDIA_ROOT / file_name

    with dest_path.open("wb") as f:
        f.write(file.file.read())

    # return public URL (served via StaticFiles)
    return f"{MEDIA_URL_BASE}/{file_name}"



# ---------- Config for image saving ----------
MEDIA_ROOT = Path(os.environ.get("PET_MEDIA_ROOT", "./pet_uploads")).absolute()
MEDIA_URL_BASE = os.environ.get("PET_MEDIA_URL_BASE", "/static/pets")  # must match StaticFiles mount
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

@router.post(
    "/",
    summary="Create pet profile",
    status_code=status.HTTP_201_CREATED,
)
def create_pet_profile(
    payload: PetProfileCreateSchema,
    db: Session = Depends(get_db),):

    existing = (
        db.query(PetProfile)
        .filter(
            PetProfile.owner == payload.owner,
            PetProfile.name == payload.name,
        )
        .first()
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error":True,
                "message": "Pet profile with this name already exists for this owner.",
            }
        )


    # Convert Enums -> plain strings for String columns
    pet_type = (
        payload.pet_type.value
        if isinstance(payload.pet_type, PetTypeEnum)
        else str(payload.pet_type)
    )
    gender = (
        payload.gender.value
        if isinstance(payload.gender, PetGenderEnum)
        else str(payload.gender)
    )
    age_range = (
        payload.age_range.value
        if isinstance(payload.age_range, PetAgeRangeEnum)
        else str(payload.age_range)
    )

    new_profile = PetProfile(
        owner=payload.owner,
        name=payload.name,
        pet_type=pet_type,
        breed=payload.breed,
        gender=gender,
        age_range=age_range,
        is_friendly_with_pets=payload.is_friendly_with_pets,
        is_friendly_with_children=payload.is_friendly_with_children,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.get(
    "/filter",
    summary="List pet profiles",
    status_code=status.HTTP_200_OK,
)
def filter(
    owner:Optional[str] = Query(None, description="Filter by owner (Appwrite user id)"),
    db:Session = Depends(get_db) 
    ):
    query = db.query(PetProfile)
    if owner:
       query = query.filter(PetProfile.owner==owner)
    
    profiles = query.order_by(PetProfile.id.desc()).all()
    return profiles


@router.put(
    "/{pet_id}",
    summary="Update pet profile",
    status_code=status.HTTP_200_OK,
)
def update_pet_profile(
    pet_id: int,
    payload: PetProfileUpdateSchema,
    db: Session = Depends(get_db),
):
    # Check if profile exists
    profile = db.query(PetProfile).filter(PetProfile.id == pet_id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "Pet profile not found"},
        )

    # If name also updated, ensure no duplicate pet name for SAME owner
    if payload.name:
        duplicate = (
            db.query(PetProfile)
            .filter(
                PetProfile.owner == profile.owner,
                PetProfile.name == payload.name,
                PetProfile.id != pet_id,  # exclude current
            )
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": True,
                    "message": "Another pet with this name already exists for this owner.",
                },
            )

    # Convert enum fields only if provided
    if payload.pet_type is not None:
        profile.pet_type = (
            payload.pet_type.value
            if isinstance(payload.pet_type, PetTypeEnum)
            else str(payload.pet_type)
        )

    if payload.gender is not None:
        profile.gender = (
            payload.gender.value
            if isinstance(payload.gender, PetGenderEnum)
            else str(payload.gender)
        )

    if payload.age_range is not None:
        profile.age_range = (
            payload.age_range.value
            if isinstance(payload.age_range, PetAgeRangeEnum)
            else str(payload.age_range)
        )

    # Update normal fields (Optional ones)
    if payload.name is not None:
        profile.name = payload.name

    if payload.breed is not None:
        profile.breed = payload.breed

    if payload.is_friendly_with_pets is not None:
        profile.is_friendly_with_pets = payload.is_friendly_with_pets

    if payload.is_friendly_with_children is not None:
        profile.is_friendly_with_children = payload.is_friendly_with_children

    # Save changes
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get("/{pet_id}/{owner}", summary="Get one pet profile by id + owner")
def getOne(
    pet_id: int,
    owner: str,
    db: Session = Depends(get_db),
):
    profile = (
        db.query(PetProfile)
        .options(joinedload(PetProfile.photos))
        .filter(
            PetProfile.id == pet_id,
            PetProfile.owner == owner,
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": True,
                "message": "Pet profile not found for this owner.",
            },
        )

    return profile

# ---------- ENDPOINTS FOR PHOTOS ----------

@router.post(
    "/{pet_id}/photos",
    summary="Upload photos for a pet",
    status_code=status.HTTP_201_CREATED,
)
async def upload_pet_photos(
    pet_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    pet = _get_pet_or_404(db, pet_id)

    created: List[PetPhotos] = []

    for file in files:
        image_url = _save_image(file)
        photo = PetPhotos(
            pet_id=pet.id,
            image=image_url,
        )
        db.add(photo)
        created.append(photo)

    db.commit()

    # refetch for clean output
    photos = (
        db.query(PetPhotos)
        .filter(PetPhotos.pet_id == pet.id)
        .order_by(PetPhotos.id.desc())
        .all()
    )
    return photos


@router.get(
    "/{pet_id}/photos",
    summary="List photos of a pet",
    status_code=status.HTTP_200_OK,
)
def list_pet_photos(
    pet_id: int,
    db: Session = Depends(get_db),
):
    _get_pet_or_404(db, pet_id)  # ensure pet exists

    photos = (
        db.query(PetPhotos)
        .filter(PetPhotos.pet_id == pet_id)
        .order_by(PetPhotos.id.desc())
        .all()
    )
    return photos


@router.delete(
    "/photos/{photo_id}",
    summary="Delete a pet photo",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_pet_photo(
    photo_id: int,
    db: Session = Depends(get_db),
):
    photo = db.query(PetPhotos).filter(PetPhotos.id == photo_id).first()
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "Photo not found"},
        )

    # Try deleting the underlying file too
    try:
        if photo.image and photo.image.startswith(MEDIA_URL_BASE):
            rel_path = photo.image.replace(MEDIA_URL_BASE, "").lstrip("/")
            file_path = MEDIA_ROOT / rel_path
            if file_path.exists():
                file_path.unlink()
    except Exception:
        # Don't fail API if file deletion fails
        pass

    db.delete(photo)
    db.commit()
    return
