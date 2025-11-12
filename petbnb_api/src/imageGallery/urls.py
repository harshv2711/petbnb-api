from typing import List, Optional
import os, uuid, shutil
from pathlib import Path
from urllib.parse import urlparse

from fastapi import (
    APIRouter, Depends, HTTPException, Query, status,
    UploadFile, File, Form, Request
)
from sqlalchemy.orm import Session

from core.database import get_db
from core.init import ImageGallery, PetHost  # adjust import paths
from pydantic import BaseModel

router = APIRouter(prefix="/image-galleries", tags=["Image Gallery"])

# ===================== Schemas =====================

class ImageGalleryBase(BaseModel):
    pet_host_id: int
    image_url: Optional[str] = None
    image_name: Optional[str] = None

class ImageGalleryOut(ImageGalleryBase):
    id: int
    class Config:
        from_attributes = True

class ImageGalleryUpdate(BaseModel):
    image_name: Optional[str] = None


# ===================== Helpers =====================

ALLOWED_IMAGE_MIME_PREFIX = "image/"
# Final path will be: MEDIA_ROOT / PARENT_DIR / HOST_SUBDIR / <id> / filename
PARENT_DIR = "pethost"
HOST_SUBDIR = "gallery-images"

def _ensure_host_exists(db: Session, host_id: int):
    host = db.query(PetHost).filter(PetHost.id == host_id).first()
    if not host:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "message": "Host account does not exist"},
        )

def _get_or_404(db: Session, gallery_id: int) -> ImageGallery:
    row = db.query(ImageGallery).filter(ImageGallery.id == gallery_id).first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": True, "message": "Image not found"},
        )
    return row

def _media_root_from_app(request: Request) -> Path:
    # Keep this consistent with main.py StaticFiles mount
    return Path(os.path.abspath(os.environ.get("MEDIA_ROOT", "./media")))

def _dest_dir_for_host(media_root: Path, host_id: int) -> Path:
    # /media/pethost/gallery-images/<host_id>/
    return media_root / PARENT_DIR / HOST_SUBDIR / str(host_id)

def _save_upload(file: UploadFile, dest_dir: Path, desired_name: Optional[str] = None) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    # choose extension
    suffix = ""
    if file.filename and "." in file.filename:
        suffix = "." + file.filename.split(".")[-1].lower()
    elif file.content_type and "/" in file.content_type:
        ext = (file.content_type.split("/")[-1] or "").lower()
        if ext:
            suffix = f".{ext}"

    base = desired_name or uuid.uuid4().hex
    safe = "".join(c for c in base if c.isalnum() or c in ("-", "_")).rstrip("_")
    name = f"{safe}{suffix}"
    path = dest_dir / name

    with path.open("wb") as out:
        shutil.copyfileobj(file.file, out)
    return path

def _public_url_for(request: Request, media_root: Path, saved_path: Path) -> str:
    # Build public URL: http(s)://host:port/media/<relative-path-from-media-root>
    rel = saved_path.relative_to(media_root).as_posix()  # e.g. pethost/gallery-images/1/abc.jpg
    base = str(request.base_url).rstrip("/")
    return f"{base}/media/{rel}"

def _file_path_from_public_url(media_root: Path, image_url: str) -> Optional[Path]:
    """
    Convert a previously-generated public URL back to a filesystem path under MEDIA_ROOT.
    Returns None if it does not map under /media.
    """
    try:
        parsed = urlparse(image_url)
        path = parsed.path.lstrip("/")  # "media/pethost/gallery-images/1/abc.jpg"
        if not path.startswith("media/"):
            return None
        rel = path[len("media/"):]
        fs_path = (media_root / rel).resolve()
        # prevent escape
        if str(fs_path).startswith(str(media_root)):
            return fs_path
        return None
    except Exception:
        return None


# ===================== CRUD Endpoints =====================

# Create (single file upload)
@router.post(
    "/upload",
    response_model=ImageGalleryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Upload one image (multipart/form-data)"
)
async def upload_one(
    request: Request,
    db: Session = Depends(get_db),
    file: UploadFile = File(..., description="Image file"),
    pet_host_id: int = Form(...),
    image_name: Optional[str] = Form(None),
):
    _ensure_host_exists(db, pet_host_id)

    if not (file.content_type or "").startswith(ALLOWED_IMAGE_MIME_PREFIX):
        raise HTTPException(status_code=415, detail={"error": True, "message": "Unsupported file type"})

    media_root = _media_root_from_app(request)
    dest_dir = _dest_dir_for_host(media_root, pet_host_id)
    saved = _save_upload(file, dest_dir, desired_name=image_name)
    public = _public_url_for(request, media_root, saved)

    row = ImageGallery(pet_host_id=pet_host_id, image_url=public, image_name=image_name or file.filename)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

# Create (multiple files)
@router.post(
    "/upload/multi",
    response_model=List[ImageGalleryOut],
    status_code=status.HTTP_201_CREATED,
    summary="Upload multiple images (multipart/form-data)"
)
async def upload_multi(
    request: Request,
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(..., description="One or more image files"),
    pet_host_id: int = Form(...),
    image_names: Optional[List[str]] = Form(None),  # pair by index if provided
):
    _ensure_host_exists(db, pet_host_id)
    media_root = _media_root_from_app(request)
    dest_dir = _dest_dir_for_host(media_root, pet_host_id)

    out_rows: List[ImageGallery] = []
    for idx, f in enumerate(files):
        if not (f.content_type or "").startswith(ALLOWED_IMAGE_MIME_PREFIX):
            raise HTTPException(status_code=415, detail={"error": True, "message": f"Unsupported: {f.filename}"})

        desired = image_names[idx] if image_names and idx < len(image_names) else None
        saved = _save_upload(f, dest_dir, desired_name=desired)
        public = _public_url_for(request, media_root, saved)

        row = ImageGallery(
            pet_host_id=pet_host_id,
            image_url=public,
            image_name=desired or f.filename
        )
        db.add(row)
        out_rows.append(row)

    db.commit()
    for r in out_rows:
        db.refresh(r)
    return out_rows

# Read (list by host)
@router.get(
    "/by-host/{pet_host_id}",
    response_model=List[ImageGalleryOut],
    summary="List all images for a host"
)
def list_by_host(
    pet_host_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(1000, ge=1, le=5000),
    offset: int = Query(0, ge=0),
):
    _ensure_host_exists(db, pet_host_id)
    q = (
        db.query(ImageGallery)
        .filter(ImageGallery.pet_host_id == pet_host_id)
        .order_by(ImageGallery.id.desc())
        .offset(offset)
        .limit(limit)
    )
    return q.all()

# Read (one)
@router.get("/{gallery_id}", response_model=ImageGalleryOut, summary="Get an image row")
def get_one(gallery_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, gallery_id)

# Update (rename etc.)
@router.patch("/{gallery_id}", response_model=ImageGalleryOut, summary="Update image row")
def update_one(gallery_id: int, payload: ImageGalleryUpdate, db: Session = Depends(get_db)):
    row = _get_or_404(db, gallery_id)
    if payload.image_name is not None:
        row.image_name = payload.image_name
    db.commit()
    db.refresh(row)
    return row

# Delete (one)
@router.delete("/{gallery_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an image")
def delete_one(
    request: Request,
    gallery_id: int,
    db: Session = Depends(get_db),
    also_delete_file: bool = Query(True, description="Remove physical file from disk too"),
):
    row = _get_or_404(db, gallery_id)

    if also_delete_file and row.image_url:
        media_root = _media_root_from_app(request)
        fs_path = _file_path_from_public_url(media_root, row.image_url)
        try:
            if fs_path and fs_path.exists():
                fs_path.unlink(missing_ok=True)
                # attempt to clean empty host dir
                host_dir = _dest_dir_for_host(media_root, row.pet_host_id)
                if host_dir.exists() and not any(host_dir.iterdir()):
                    host_dir.rmdir()
        except Exception:
            pass

    db.delete(row)
    db.commit()
    return None

# Delete (all for host)
@router.delete(
    "/by-host/{pet_host_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete all images for a host"
)
def delete_all_for_host(
    request: Request,
    pet_host_id: int,
    db: Session = Depends(get_db),
    also_delete_files: bool = Query(True, description="Remove physical files from disk too"),
):
    _ensure_host_exists(db, pet_host_id)
    rows = (
        db.query(ImageGallery)
        .filter(ImageGallery.pet_host_id == pet_host_id)
        .all()
    )

    if also_delete_files:
        media_root = _media_root_from_app(request)
        for r in rows:
            try:
                if r.image_url:
                    fs_path = _file_path_from_public_url(media_root, r.image_url)
                    if fs_path and fs_path.exists():
                        fs_path.unlink(missing_ok=True)
            except Exception:
                pass
        # try to remove the (now empty) dir
        try:
            host_dir = _dest_dir_for_host(media_root, pet_host_id)
            if host_dir.exists() and not any(host_dir.iterdir()):
                host_dir.rmdir()
        except Exception:
            pass

    for r in rows:
        db.delete(r)
    db.commit()
    return None
