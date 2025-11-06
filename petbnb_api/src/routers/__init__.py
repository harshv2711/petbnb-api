from petHost.urls import router as petHostRouter
from booking.urls import router as bookingRouter
from petPreference.urls import router as petPreferenceRouter
from service.urls import router as petServiceRouter
from imageGallery.urls import router as petHostImageGalleryRouter
from petProfile.urls import router as petProfileRouter


__all__ = [
    "petHostRouter", 
    "bookingRouter", 
    "petPreferenceRouter", 
    "petServiceRouter",
    "petHostImageGalleryRouter",
    "petProfileRouter",
]