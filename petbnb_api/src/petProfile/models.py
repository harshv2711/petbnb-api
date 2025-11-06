from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from core.database import Base


class PetProfile(Base):
    __tablename__ = "pet_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)  # assuming 'users' table exists
    pet_name = Column(String, nullable=False)
    pet_type = Column(String, nullable=True)
    pet_age = Column(String, nullable=True)
    breed = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    weight_kg = Column(Float, nullable=True)

    is_vaccinated = Column(Boolean, default=True)
    is_friendly_with_children = Column(Boolean, default=True)
    pet_profile_image_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="pet_profiles")

    # Linked images
    images = relationship(
        "PetImage",
        back_populates="pet_profile",
        cascade="all, delete-orphan"
    )


class PetImage(Base):
    __tablename__ = "pet_images"

    id = Column(Integer, primary_key=True, index=True)
    pet_profile_id = Column(Integer, ForeignKey("pet_profiles.id", ondelete="CASCADE"), nullable=False)

    image_url = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    pet_profile = relationship("PetProfile", back_populates="images")
