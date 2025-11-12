from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field


class ImageGalleryBase(BaseModel):
    image_url: Optional[HttpUrl] = Field(None, description="Publicly accessible image URL")
    image_name: Optional[str] = Field(None, max_length=255)


class ImageGalleryCreate(ImageGalleryBase):
    pet_host_id: int
    image_url: HttpUrl  # required on create


class ImageGalleryUpdate(ImageGalleryBase):
    # partial update
    pass


class ImageGalleryOut(ImageGalleryBase):
    id: int
    pet_host_id: int

    class Config:
        from_attributes = True  # Pydantic v2
