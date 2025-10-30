from pydantic import BaseModel
from imageGallery.models import ImageGallery
from service.models import ServiceOffer

class hostProfileSchema(BaseModel):
    id: int
    image_gallery: ImageGallery
    profile_image: str
    first_name: bool
    last_name: bool
    service_offers: ServiceOffer
    rating: int
    address: str
    account_status: str
    is_verified: bool