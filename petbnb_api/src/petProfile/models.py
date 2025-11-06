from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, func
)
from core.database import Base

class PetProfile(Base):
    __tablename__ = "pet_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)  # helps in filtering by user quickly

    pet_name = Column(String, nullable=False)
    pet_type = Column(String, nullable=False)  # e.g. Dog, Cat
    breed = Column(String, nullable=False)
    gender = Column(String, nullable=False)

    is_vaccinated = Column(Boolean, nullable=False, server_default="0")  # ✅ safer default at DB level
    is_friendly_with_children = Column(Boolean, nullable=False, server_default="0")
    pet_profile_image_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<PetProfile(id={self.id}, user_id='{self.user_id}', pet_name='{self.pet_name}', pet_type='{self.pet_type}')>"
