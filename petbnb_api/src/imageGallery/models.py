# database.py
from sqlalchemy import (
    Column, Integer, String,
    DateTime, func, ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base

class ImageGallery(Base):
    __tablename__ = "image_galleries"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)
    image_url = Column(String)
    image_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    pet_host = relationship("PetHost", back_populates="image_gallery")

