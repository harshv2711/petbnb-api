from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.database import Base


class PetProfile(Base):
    __tablename__ = "pet_profiles"

    id = Column(Integer, primary_key=True, index=True)

    # Appwrite User ID of the pet owner
    owner = Column(String, nullable=False, index=True)

    # ---------- Pet Details ----------
    name = Column(String, nullable=False)
    pet_type = Column(String, nullable=False)       # Dog / Cat / Other
    breed = Column(String, nullable=False)
    gender = Column(String, nullable=False)         # Male / Female / Other
    age_range = Column(String, nullable=False)      # Puppy / Adult / Senior

    # ---------- Health & Safety ----------
    # is_vaccinated = Column(Boolean, nullable=False, default=False)
    # is_any_medical_conditions = Column(Boolean, nullable=False, default=False)
    # medical_conditions_details = Column(Text, nullable=True)
    # allergies = Column(Text, nullable=True)

    # ---------- Behavior & Preferences ----------
    is_friendly_with_pets = Column(Boolean, nullable=False, default=False)
    is_friendly_with_children = Column(Boolean, nullable=False, default=False)
    # energy_level = Column(String, nullable=True)  # Low / Medium / High
    # trained = Column(Boolean, nullable=False, default=False)
    # feeding_instructions = Column(Text, nullable=True)
    # walking_preferences = Column(Text, nullable=True)

    # ---------- Relationship ----------
    photos = relationship("PetPhotos", back_populates="pet", cascade="all, delete")


class PetPhotos(Base):
    __tablename__ = "pet_photos"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pet_profiles.id"), nullable=False)
    image = Column(String, nullable=False)  # URL or local path
    pet = relationship("PetProfile", back_populates="photos")
