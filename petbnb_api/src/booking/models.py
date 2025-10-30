# database.py
from sqlalchemy import (
    Column, Integer, Float, Boolean, String,
    DateTime, func, ForeignKey
)
from sqlalchemy.orm import relationship
from core.database import Base
from pydantic import BaseModel, HttpUrl
from enum import Enum
from utils import PricingBasisEnum, PetTypeEnum, PetGenderEnum
from typing import Optional


class ServiceOfferSchema(BaseModel):
    # id: int
    pet_host_id: int
    service_name: str
    service_description: str
    service_price: float
    pricing_basis: PricingBasisEnum

    class Config:
        orm_mode = True

class Booking(BaseModel):
    id: int # primary key
    bookingNumber: int # like OrderId
    userId: int # pet owner 
    petHostId: int # Booked this host
    # for service 
    service_name: str # boarding, walking or training
    service_price: float # 999.0
    pricing_basis: PricingBasisEnum
    checkInAt: DateTime
    checkOutInAt: DateTime
    totalAmt: float # 1245 add platform fee and GST
    
    # for pet profile

class PetProfiel:
    id: int
    petProfileImageUrl: Optional[HttpUrl] = None
    petName: str # buro -  Dog male golden retriver 5 Years 25kg Vaccinated
    petType: PetTypeEnum
    gender: PetGenderEnum
    breed: str
    age: str
    weightKg: str
    isVaccinated: bool
    isFriendlyWithChildren: bool



    