from petHost.urls import router as petHostRouter
from booking.urls import router as bookingRouter
from petPreference.urls import router as petPreferenceRouter
from service.urls import router as petServiceRouter

__all__ = [
    "petHostRouter", 
    "bookingRouter", 
    "petPreferenceRouter", 
    "petServiceRouter",
]