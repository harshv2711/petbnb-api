# database.py
from sqlalchemy import (
    Column, Integer, Float, String,
    DateTime, func, ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base


class ServiceOffer(Base):
    __tablename__ = "service_offer"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)
    service_name = Column(String)
    service_description = Column(String)
    service_price = Column(Float)
    pricing_basis = Column(String)  # "Per hour" | "Per day" | "Per session"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    pet_host = relationship("PetHost", back_populates="service_offers")
