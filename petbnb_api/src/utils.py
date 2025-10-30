
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


class PetGenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "other"
