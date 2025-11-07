from pydantic import BaseModel
from typing import List, Optional
import enum


# ======================
# ENUM CLASSES
# ======================
class BookingStatusEnum(str, enum.Enum):
    waiting = "waiting"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    ongoing = "ongoing"


class PaymentStatusEnum(str, enum.Enum):
    unpaid = "unpaid"
    pending = "pending"
    paid = "paid"
    refunded = "refunded"
    partially_refunded = "partiallyRefunded"
    failed = "failed"
    disputed = "disputed"
    expired = "expired"


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


# ======================
# NESTED SERVICE SCHEMA
# ======================
class ServiceBookingSchema(BaseModel):
    service_name: str
    service_amt: float
    amt_basis: str


# ======================
# MAIN BOOKING SCHEMA
# ======================
class BookingCreateSchema(BaseModel):
    booking_uuid: str
    user_id: str
    booked_pet_host_id: int
    booked_for_service: List[ServiceBookingSchema]
    booked_for_pet_profiles: List[int]
    booking_status: BookingStatusEnum = BookingStatusEnum.waiting
    payment_status: PaymentStatusEnum = PaymentStatusEnum.unpaid
    cancelled_by: Optional[CancelledByEnum] = None
    is_canceled: bool = False

    class Config:
        orm_mode = True
