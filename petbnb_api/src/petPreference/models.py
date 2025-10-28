# database.py
from sqlalchemy import (
    Column, Integer, Float, Boolean, String,
    DateTime, func, ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base

class PetPreferences(Base):
    __tablename__ = "pet_preferences"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), unique=True, nullable=False)
    pet_type = Column(String)           # Dog, Cat, Both
    pet_size_accepted = Column(String)  # Small, Medium, Large
    age_range = Column(String)          # Puppy, Adult, Senior
    special_needs_pet_accepted = Column(Boolean, default=True)
    medical_needs_pet_accepted = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    pet_host = relationship("PetHost", back_populates="pet_preferences")


