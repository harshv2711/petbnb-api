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


class CreateHostAccountInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str


