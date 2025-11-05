from petHost.urls import router as petHostRouter
from booking.urls import router as bookingRouter
from petPreference.urls import router as petPreferenceRouter

__all__ = ["petHostRouter", "bookingRouter", "petPreferenceRouter"]