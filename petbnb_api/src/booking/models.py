from pydantic import BaseModel
import enum
from core.database import Base
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey, func
)
from sqlalchemy.orm import relationship


# =========================
# ENUM CLASSES
# =========================
class BookingStatusEnum(str, enum.Enum):
    waiting = "waiting"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    ongoing = "ongoing"


class CancelledByEnum(str, enum.Enum):
    pet_host = "petHost"
    pet_owner = "petOwner"
    platform = "platform"
    system_auto = "systemAuto"
    payment_failure = "paymentFailure"
    policy_violation = "policyViolation"
    duplicate_booking = "duplicateBooking"
    weather_issue = "weatherIssue"
    other = "other"


class PaymentStatusEnum(str, enum.Enum):
    unpaid = "unpaid"
    pending = "pending"
    paid = "paid"
    refunded = "refunded"
    partially_refunded = "partiallyRefunded"
    failed = "failed"
    disputed = "disputed"
    expired = "expired"


# =========================
# DATABASE MODELS
# =========================
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_uuid = Column(String, unique=True, nullable=False)  # UUID string
    user_id = Column(String, nullable=False)
    booked_pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)

    booking_status = Column(String, default=BookingStatusEnum.waiting.value)
    payment_status = Column(String, default=PaymentStatusEnum.unpaid.value)
    cancelled_by = Column(String, nullable=True)
    is_canceled = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    booked_pet_host = relationship("PetHost", back_populates="bookings")
    services = relationship("BookingService", back_populates="booking", cascade="all, delete")
    pets = relationship("BookingPetProfile", back_populates="booking", cascade="all, delete")


class BookingService(Base):
    __tablename__ = "booking_services"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    service_name = Column(String, nullable=False)  # e.g. Boarding, Grooming
    service_amt = Column(Float, nullable=False)
    amt_basis = Column(String, nullable=False)  # e.g. per night, per hour

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    booking = relationship("Booking", back_populates="services")


class BookingPetProfile(Base):
    __tablename__ = "booking_pet_profiles"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    pet_profile_id = Column(Integer, ForeignKey("pet_profiles.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    booking = relationship("Booking", back_populates="pets")
    pet_profile = relationship("PetProfile")


# =========================
# PYDANTIC SCHEMAS
# =========================
class HostServiceBooking(BaseModel):
    service_name: str
    service_amt: float
    amt_basis: str


class BookingSchema(BaseModel):
    booking_uuid: str
    user_id: str
    booked_pet_host_id: int
    booked_for_service: list[HostServiceBooking]
    booked_for_pet_profiles: list[int]  # list of pet profile IDs

    booking_status: BookingStatusEnum = BookingStatusEnum.waiting
    payment_status: PaymentStatusEnum = PaymentStatusEnum.unpaid
    cancelled_by: CancelledByEnum | None = None
    is_canceled: bool = False

    class Config:
        orm_mode = True
