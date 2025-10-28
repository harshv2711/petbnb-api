from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.init import (
    PetHost,
    PetPreferences,
    ServiceOffer,
    ImageGallery,
    Certification,
    ReviewsAndRating,
)

# --- Sample seed data ---
FIRST_NAMES = ["Aarav", "Vihaan", "Vivaan", "Aditya", "Arjun",
               "Reyansh", "Muhammad", "Sai", "Krishna", "Ishaan"]
LAST_NAMES = ["Sharma", "Mehta", "Iyer", "Patel", "Khan",
              "Singh", "Joshi", "Nair", "Kapoor", "Rao"]

ADDRESSES = [
    "Andheri West, Mumbai",
    "Powai, Mumbai",
    "Baner, Pune",
    "Kalyani Nagar, Pune",
    "BTM Layout, Bengaluru",
    "HSR Layout, Bengaluru",
    "Jayanagar, Bengaluru",
    "Gachibowli, Hyderabad",
    "Kukatpally, Hyderabad",
    "Kharadi, Pune",
]

LANGUAGES = [
    "English, Hindi, Marathi",
    "English, Hindi, Gujarati",
    "English, Hindi, Tamil",
    "English, Hindi",
    "English, Hindi, Kannada",
    "English, Hindi",
    "English, Hindi, Malayalam",
    "English, Hindi, Telugu",
    "English, Hindi",
    "English, Hindi, Marathi",
]


# --- Helper factories ---

def mk_services(i: int) -> List[ServiceOffer]:
    base = (i % 3) + 1
    return [
        ServiceOffer(
            service_name="Boarding",
            service_description="Overnight pet stay with 2 walks and regular updates.",
            service_price=1000 + base * 50,
            pricing_basis="Per day",
        ),
        ServiceOffer(
            service_name="Daycare",
            service_description="Daytime care, playtime, and meals per schedule.",
            service_price=600 + base * 40,
            pricing_basis="Per day",
        ),
        ServiceOffer(
            service_name="Dog Walking",
            service_description="Neighbourhood walk with photo updates.",
            service_price=200 + base * 20,
            pricing_basis="Per session",
        ),
    ]


def mk_images(i: int) -> List[ImageGallery]:
    return [
        ImageGallery(
            image_url=f"https://example.com/images/host{i+1}_home.jpg",
            image_name="Living Room",
        ),
        ImageGallery(
            image_url=f"https://example.com/images/host{i+1}_yard.jpg",
            image_name="Backyard",
        ),
    ]


def mk_certs(i: int) -> List[Certification]:
    return [
        Certification(
            certificate_name="Pet First Aid & CPR",
            certificate_url=f"https://example.com/certs/host{i+1}_cpr.pdf",
            certificate_description="Certified basic first aid for pets.",
        ),
        Certification(
            certificate_name="Canine Behaviour Basics",
            certificate_url=f"https://example.com/certs/host{i+1}_behaviour.pdf",
            certificate_description="Intro course on dog behaviour and handling.",
        ),
    ]


def mk_reviews(i: int) -> List[ReviewsAndRating]:
    return [
        ReviewsAndRating(
            star_rating=5 - (i % 2),
            review_title="Great experience",
            review_text="Very caring and timely updates. Highly recommended!",
        ),
        ReviewsAndRating(
            star_rating=4,
            review_title="Good host",
            review_text="Nice home, my pet was comfortable and happy.",
        ),
    ]


def mk_preferences(i: int) -> PetPreferences:
    pet_type = ["Dog", "Cat", "Both"][i % 3]
    size = ["Small", "Medium", "Large"][i % 3]
    age = ["Puppy", "Adult", "Senior"][i % 3]
    return PetPreferences(
        pet_type=pet_type,
        pet_size_accepted=size,
        age_range=age,
        special_needs_pet_accepted=(i % 2 == 0),
        medical_needs_pet_accepted=True,
    )


def mk_host(i: int) -> PetHost:
    first = FIRST_NAMES[i]
    last = LAST_NAMES[i]
    email = f"{first.lower()}.{last.lower()}@example.com"
    rating_int = 4 if i % 3 else 5

    host = PetHost(
        user_id=f"USR_{1023 + i}",
        first_name=first,
        last_name=last,
        email=email,
        mobile_number=f"+91-98{i:02d}{(76543210 + i) % 100000000:08d}",
        bio="Animal lover with experience caring for dogs and cats. Safe, homely environment with regular photo/video updates.",
        experience=f"{(i % 6) + 1} Years",
        address=ADDRESSES[i],
        account_status="active",
        rating=rating_int,
        profile_image=f"https://example.com/images/{first.lower()}_{last.lower()}.jpg",
        is_verified=(i % 2 == 0),
        number_of_pet_hosted=20 + i * 3,
        hosting_capacity=2 + (i % 3),
        language=LANGUAGES[i],
        availability_status="available" if i % 4 != 0 else "on_leave",
        is_superhost=(i % 3 == 0),
        total_review=10 + i,
        total_earnings=75000.0 + (i * 3250.5),
    )

    # Attach relationships
    host.pet_preferences = mk_preferences(i)
    host.service_offers = mk_services(i)
    host.image_gallery = mk_images(i)
    host.certifications = mk_certs(i)
    host.reviews = mk_reviews(i)

    return host


# --- Seeder main function ---

def main():
    db: Session = SessionLocal()
    try:
        hosts = [mk_host(i) for i in range(10)]

        db.add_all(hosts)
        db.commit()

        for h in hosts:
            db.refresh(h)

        print("✅ Seed complete. Inserted PetHosts with IDs:")
        print([h.id for h in hosts])

    except Exception as e:
        db.rollback()
        print("❌ Seed failed:", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
