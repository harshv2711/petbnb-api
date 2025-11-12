from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class PetTypeEnum(str, Enum):
    Dog = "Dog"
    Cat = "Cat"
    Both = "Both"


class PetSizeEnum(str, Enum):
    Small = "Small"
    Medium = "Medium"
    Large = "Large"
    All = "All"



class AgeRangeEnum(str, Enum):
    Puppy = "Puppy"
    Adult = "Adult"
    Senior = "Senior"
    All = "All"


# ---------- In / Out Schemas ----------

class PetPreferencesBase(BaseModel):
    pet_type: Optional[PetTypeEnum] = Field(None, description="Dog, Cat, or Both")
    pet_size_accepted: Optional[PetSizeEnum] = Field(None, description="Small, Medium, Large, All")
    age_range: Optional[AgeRangeEnum] = Field(None, description="Puppy, Adult, Senior")
    special_needs_pet_accepted: Optional[bool] = True
    medical_needs_pet_accepted: Optional[bool] = True


class PetPreferencesCreate(PetPreferencesBase):
    pet_host_id: int


class PetPreferencesUpdate(PetPreferencesBase):
    # All fields optional for PATCH
    pass


class PetPreferencesOut(PetPreferencesBase):
    id: int
    pet_host_id: int

    class Config:
        from_attributes = True  # Pydantic v2 (for SQLAlchemy models)
