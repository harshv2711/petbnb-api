from pydantic import BaseModel, EmailStr
from enum import Enum


# ---------- ENUMS ----------
class AccountStatusEnum(str, Enum):
    UNDER_REVIEW = "under_review"             # Profile just created and awaiting admin approval
    ACTIVE = "active"                         # Host is verified and visible in search results
    INACTIVE = "inactive"                     # Host has deactivated temporarily
    ON_LEAVE = "on_leave"                     # Host is temporarily unavailable to take bookings
    BLOCKED = "blocked"                       # Host account disabled due to violation or issues
    PENDING_VERIFICATION = "pending_verification"  # Awaiting identity / KYC verification
    SUSPENDED = "suspended"                   # Suspended for a fixed period due to quality issue


class PetTypeEnum(str, Enum):
    DOG = "Dog"
    CAT = "Cat"
    BOTH = "Both"


class AgeRangeEnum(str, Enum):
    PUPPY = "Puppy"
    ADULT = "Adult"
    SENIOR = "Senior"


class PetSizeAcceptedEnum(str, Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class PricingBasisEnum(str, Enum):
    PER_HOUR = "Per hour"
    PER_DAY = "Per day"
    PER_SESSION = "Per session"


# ---------- SCHEMAS ----------
class PetHostSchema(BaseModel):
    # id: str
    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    bio: str
    experience: str
    account_status: AccountStatusEnum
    rating: int
    profile_image: str
    is_verified: bool
    number_of_pet_hosted: int
    hosting_capacity: int
    language: str
    availability_status: str
    is_superhost: bool
    total_review: int
    total_earnings: float

    class Config:
        orm_mode = True


class PetPreferencesSchema(BaseModel):
    # id: int
    pet_host_id: int
    pet_type: PetTypeEnum
    pet_size_accepted: PetSizeAcceptedEnum
    age_range: AgeRangeEnum
    special_needs_pet_accepted: bool
    medical_needs_pet_accepted: bool

    class Config:
        orm_mode = True


class CertificationSchema(BaseModel):
    id: int
    pet_host_id: int
    certificate_name: str
    certificate_url: str
    certificate_description: str

    class Config:
        orm_mode = True


class ServiceOfferSchema(BaseModel):
    # id: int
    pet_host_id: int
    service_name: str
    service_description: str
    service_price: float
    pricing_basis: PricingBasisEnum

    class Config:
        orm_mode = True
