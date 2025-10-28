# database.py
from sqlalchemy import (
    Column, Integer, String,
    DateTime, func, ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)
    certificate_name = Column(String)
    certificate_url = Column(String)
    certificate_description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    pet_host = relationship("PetHost", back_populates="certifications")

