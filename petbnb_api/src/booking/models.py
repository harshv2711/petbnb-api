from pydantic import BaseModel
import enum

class BookingStatusEnum(str, enum.Enum):
    waiting = "waiting"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    ongoing = "ongoing"


class CancelledByEnum(str, enum.Enum):
    pet_host = "petHost"                  # Host cancelled (e.g., unavailable or emergency)
    pet_owner = "petOwner"                # Owner cancelled (e.g., travel plan changed)
    platform = "platform"                 # Admin manually cancelled
    system_auto = "systemAuto"            # Auto-cancel due to timeout or no response
    payment_failure = "paymentFailure"    # Cancelled automatically because payment failed
    policy_violation = "policyViolation"  # Cancelled due to fraud, T&C breach, or misconduct
    duplicate_booking = "duplicateBooking" # Cancelled because duplicate was detected
    weather_issue = "weatherIssue"        # Cancelled due to severe weather/natural causes
    other = "other"                       # Fallback for uncategorized reasons

class PaymentStatusEnum(str, enum.Enum):
    unpaid = "unpaid"                 # Booking created, payment not yet made
    pending = "pending"               # Payment initiated but not confirmed
    paid = "paid"                     # Successfully paid and confirmed
    refunded = "refunded"             # Fully refunded
    partially_refunded = "partiallyRefunded"  # Partial refund issued
    failed = "failed"                 # Payment attempt failed
    disputed = "disputed"             # Payment under dispute or chargeback
    expired = "expired" 


class HostService:
    pass              # Payment link expired or timed out

class PetProfile:
    pass

class HostServiceBooking(BaseModel):
    id: int
    bookingUUID: str
    serviceName: str
    serviceAmt: float
    amt_basis: str

class Booking(BaseModel):
    id: int
    bookingUUID: str #random UUID same as Order to track Booking
    userID: str # person who booked a particular host
    bookedPetHost: int # pet Host Id
    bookedForService: list[HostServiceBooking]
    bookedForPetProfiles: list[PetProfile]

    bookingStatus: BookingStatusEnum 
    paymentStatus: PaymentStatusEnum
    cancelledBy: CancelledByEnum
    isCanceled: bool = False



