from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field
from core.database import get_db
from core.init import PetHost, ImageGallery  # adjust if your models live elsewhere

router = APIRouter(prefix="/gallery", tags=["Image Gallery"])

# ---------- SCHEMAS ----------
class ImageItem(BaseModel):
    image_name: str = Field(..., min_length=2, max_length=120)
    image_url: str = Field(..., min_length=5)

class GalleryBulkInput(BaseModel):
    user_id: str
    images: List[ImageItem]

class DeleteImageByNameSchema(BaseModel):
    user_id: str


# ---------- BULK UPSERT (CREATE or UPDATE by image_name) ----------
@router.post("/")
def upsert_images(
    payload: GalleryBulkInput,
    db: Session = Depends(get_db)
):
    # 1) Verify host
    host = db.query(PetHost).filter(PetHost.user_id == payload.user_id).first()
    if not host:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "message": "Host account does not exist"}
        )

    # 2) Load existing images once
    existing = (
        db.query(ImageGallery)
        .filter(ImageGallery.pet_host_id == host.id)
        .all()
    )
    existing_by_name = {img.image_name.lower().strip(): img for img in existing}

    created, updated = 0, 0
    touched: list[ImageGallery] = []

    # 3) Upsert each incoming image by image_name
    for item in payload.images:
        key = item.image_name.lower().strip()
        if key in existing_by_name:
            # Update URL for existing name
            rec = existing_by_name[key]
            rec.image_url = item.image_url
            updated += 1
            touched.append(rec)
        else:
            # Create new record
            rec = ImageGallery(
                pet_host_id=host.id,
                image_name=item.image_name.strip(),
                image_url=item.image_url
            )
            db.add(rec)
            created += 1
            touched.append(rec)

    db.commit()
    for r in touched:
        db.refresh(r)

    return {
        "message": "Image gallery upserted successfully",
        "summary": {"created": created, "updated": updated, "total": len(touched)},
        "data": touched
    }


# ---------- DELETE by ID ----------
@router.delete("/item/{image_id}")
def delete_image_by_id(
    image_id: int,
    db: Session = Depends(get_db)
):
    rec = db.query(ImageGallery).filter(ImageGallery.id == image_id).first()
    if not rec:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "message": "Image not found"}
        )

    db.delete(rec)
    db.commit()
    return {"message": "Image deleted successfully", "deleted_image_id": image_id}


# ---------- DELETE by NAME for a host ----------
@router.delete("/item/by-name/{image_name}")
def delete_image_by_name(
    image_name: str,
    payload: DeleteImageByNameSchema,
    db: Session = Depends(get_db)
):
    host = db.query(PetHost).filter(PetHost.user_id == payload.user_id).first()
    if not host:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "message": "Host account does not exist"}
        )

    rec = (
        db.query(ImageGallery)
        .filter(
            ImageGallery.pet_host_id == host.id,
            ImageGallery.image_name == image_name
        )
        .first()
    )
    if not rec:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "message": f"Image '{image_name}' not found"}
        )

    db.delete(rec)
    db.commit()
    return {"message": f"Image '{image_name}' deleted successfully", "deleted_image_name": image_name}
