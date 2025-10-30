from pydantic import BaseModel
from enum import Enum

class PricingBasisEnum(str, Enum):
    PER_HOUR = "Per hour"
    PER_DAY = "Per day"
    PER_SESSION = "Per session"


class BookingDetailsInputSchema(BaseModel):
    id: int 
    userId: int # pet owner
    petHostId: int # who booked pet host
    serviceName: str
    servicePrice: float
    pricingBasis: PricingBasisEnum
