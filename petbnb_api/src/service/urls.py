from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Literal
from pydantic import BaseModel, Field
from core.init import PetHost, ServiceOffer
from core.database import get_db

router = APIRouter(prefix="/service", tags=["Service Offer"])


# ---------- SCHEMAS ----------
class ServiceOfferItem(BaseModel):
    service_name: str = Field(..., min_length=2, max_length=80)
    service_price: float = Field(..., ge=0)
    pricing_basis: Literal["Per hour", "Per day", "Per session"]


class PetServiceInputSchema(BaseModel):
    user_id: str
    services: List[ServiceOfferItem]


# ---------- ROUTE ----------
@router.post("/")
def setPetService(
    petServiceData: PetServiceInputSchema,
    db: Session = Depends(get_db)
):
    # Step 1: Verify host exists
    existingHost = db.query(PetHost).filter(PetHost.user_id == petServiceData.user_id).first()
    if not existingHost:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": "Host account does not exist"
            }
        )

    # Step 2: Fetch existing services for this host
    existingServices = (
        db.query(ServiceOffer)
        .filter(ServiceOffer.pet_host_id == existingHost.id)
        .all()
    )
    existing_by_name = {s.service_name.lower().strip(): s for s in existingServices}

    created, updated = 0, 0
    upserted_records: list[ServiceOffer] = []

    # Step 3: Upsert each service
    for item in petServiceData.services:
        key = item.service_name.lower().strip()
        if key in existing_by_name:
            # Update existing record
            svc = existing_by_name[key]
            svc.service_price = item.service_price
            svc.pricing_basis = item.pricing_basis
            updated += 1
            upserted_records.append(svc)
        else:
            # Create new service record
            svc = ServiceOffer(
                pet_host_id=existingHost.id,
                service_name=item.service_name.strip(),
                service_price=item.service_price,
                pricing_basis=item.pricing_basis
            )
            db.add(svc)
            created += 1
            upserted_records.append(svc)

    # Step 4: Commit all changes
    db.commit()

    # Step 5: Refresh all records
    for record in upserted_records:
        db.refresh(record)

    return {
        "message": "Service offers upserted successfully",
        "summary": {
            "created": created,
            "updated": updated,
            "total": len(upserted_records)
        },
        "data": upserted_records
    }


@router.delete("/item/{service_id}")
def delete_service_by_id(
    service_id: int,
    db: Session = Depends(get_db)
):
    # Step 1: Find the service
    svc = db.query(ServiceOffer).filter(ServiceOffer.id == service_id).first()
    if not svc:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "message": "Service not found"}
        )

    # Step 2: Delete the service
    db.delete(svc)
    db.commit()

    return {
        "message": "Service deleted successfully",
        "deleted_service_id": service_id
    }
