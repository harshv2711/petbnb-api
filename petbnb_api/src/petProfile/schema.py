from pydantic import BaseModel
import enum


class PetAgeRangeEnum(enum.Enum):
    Puppy = "Puppy"
    ADULT = "Adult"
    SENIOR = "Senior"

class PetGenderEnum(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class PetTypeEnum(enum.Enum):
    DOG = "Dog"
    CAT = "Cat"
    ALL = "All"


class PetProfileCreateSchema(BaseModel):
    owner: str # appwrite user id
    name: str
    pet_type: PetTypeEnum
    breed: str
    gender: PetGenderEnum
    age_range: PetAgeRangeEnum
    is_friendly_with_pets: bool
    is_friendly_with_children: bool


class PetProfileUpdateSchema(BaseModel):
    owner: str # appwrite user id
    name: str
    pet_type: PetTypeEnum
    breed: str
    gender: PetGenderEnum
    age_range: PetAgeRangeEnum
    is_friendly_with_pets: bool
    is_friendly_with_children: bool



