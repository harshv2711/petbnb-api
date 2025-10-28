# database.py
from sqlalchemy import (
    Column, Integer, String,
    DateTime, func, ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base

class ReviewsAndRating(Base):
    __tablename__ = "reviews_and_rating"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)
    star_rating = Column(Integer, default=0)
    review_title = Column(String)
    review_text = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    pet_host = relationship("PetHost", back_populates="reviews")


