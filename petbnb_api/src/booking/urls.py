from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.init import Booking, BookingService, BookingPetProfile
from .schemas import BookingCreateSchema
from core.init import PetHost, PetProfile  # Assuming these exist
import uuid

router = APIRouter(prefix="/booking", tags=["Booking"])


@router.post("/", response_model=dict)
def create_booking(payload: BookingCreateSchema, db: Session = Depends(get_db)):
    # ✅ Check if Pet Host exists
    host = db.query(PetHost).filter(PetHost.id == payload.booked_pet_host_id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Pet Host not found")

    # ✅ Validate Pet Profiles
    for pet_id in payload.booked_for_pet_profiles:
        pet = (db.query(PetProfile)
               .filter(PetProfile.id == pet_id)
               .filter(PetProfile.user_id == payload.user_id)
               .first())
        if not pet:
            raise HTTPException(status_code=404, detail=f"Pet Profile {pet_id} not found")

    # ✅ Create main Booking record
    new_booking = Booking(
        booking_uuid=payload.booking_uuid or str(uuid.uuid4()),
        user_id=payload.user_id,
        booked_pet_host_id=payload.booked_pet_host_id,
        booking_status=payload.booking_status.value,
        payment_status=payload.payment_status.value,
        cancelled_by=payload.cancelled_by.value if payload.cancelled_by else None,
        is_canceled=payload.is_canceled,
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # ✅ Create Booking Services
    for service in payload.booked_for_service:
        db_service = BookingService(
            booking_id=new_booking.id,
            service_name=service.service_name,
            service_amt=service.service_amt,
            amt_basis=service.amt_basis,
        )
        db.add(db_service)

    # ✅ Create Booking Pet Profiles
    for pet_id in payload.booked_for_pet_profiles:
        db_pet = BookingPetProfile(
            booking_id=new_booking.id,
            pet_profile_id=pet_id
        )
        db.add(db_pet)

    db.commit()

    return {
        "error": False,
        "message": "Booking created successfully",
        "booking_id": new_booking.id,
        "booking_uuid": new_booking.booking_uuid
    }
