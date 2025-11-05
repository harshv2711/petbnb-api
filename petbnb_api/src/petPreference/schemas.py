from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum

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


class CreatePetPreferenceInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    pet_type: PetTypeEnum
    pet_size_accepted: PetSizeAcceptedEnum
    age_range: AgeRangeEnum
    special_needs_pet_accepted: bool
    medical_needs_pet_accepted: bool
