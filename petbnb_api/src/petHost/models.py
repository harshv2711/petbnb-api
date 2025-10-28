# database.py
from sqlalchemy import (
    Column, Integer, Float, Boolean, String,
    DateTime, func, ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base

class PetHost(Base):
    __tablename__ = "pet_hosts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    mobile_number = Column(String)
    bio = Column(String)
    experience = Column(String)
    address = Column(String)
    account_status = Column(String, default="under_review")
    rating = Column(Integer, default=0)
    profile_image = Column(String)
    is_verified = Column(Boolean, default=False)
    number_of_pet_hosted = Column(Integer, default=0)
    hosting_capacity = Column(Integer, default=1)
    language = Column(String)
    availability_status = Column(String, default="available")
    is_superhost = Column(Boolean, default=False)
    total_review = Column(Integer, default=0)
    total_earnings = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # -------- Relationships (attached collections/objects) --------
    pet_preferences = relationship(
        "PetPreferences",
        back_populates="pet_host",
        uselist=False,            # one-to-one
        cascade="all, delete-orphan",
        lazy="joined"             # grab with the host (1:1 is cheap to join)
    )
    certifications = relationship(
        "Certification",
        back_populates="pet_host",
        cascade="all, delete-orphan",
        lazy="selectin"           # efficient one-to-many loading
    )
    service_offers = relationship(
        "ServiceOffer",
        back_populates="pet_host",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    image_gallery = relationship(
        "ImageGallery",
        back_populates="pet_host",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    reviews = relationship(
        "ReviewsAndRating",
        back_populates="pet_host",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

