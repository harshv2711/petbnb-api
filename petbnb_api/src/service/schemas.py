from pydantic import BaseModel

class PetServiceInputSchema(BaseModel):
    pet_host_id:int
    service_name: str
    service_price: float
    pricing_basis: str
    