from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean


class PetHost(Base):

    __tablename__ = "petHosts"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    mobileNumber = Column(String)
    bio = Column(String)
    experience = Column(String)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    accountStatus = Column(String) #['active', 'blocked', 'under_review']
    rating = Float(String)
    profileImage = Column(String)
    isVerified = Column(Boolean, default=False)
    numberOfPetHosted = Column(Integer, default=0)
    hosting_capacity = Column(Integer, default=1)
    languages = Column(String) #["English", "Hindi", "Marathi"]
    # petPreferences = PetPreferences()
    # certification = Certification()
    # serviceOffer = ServiceOffer()
    # imageGallery = ImageGallery()
    availabilityStatus = Column(String) # ["available", "unavailable", "on_leave"]
    isSuperhost = Column(Boolean, default=False)
    total_reviews = Column(Integer, default=0)
    createdAt = ""
    updatedAt = ""
    reviewsAndRating = []
    totalEarnings = Column(Float)


class PetPreferences(Base):
    id = Column(Integer, primary_key=True, index=True)
    petHostId = Column(Integer, foreign_key=True)
    petType = ["Dog, Cat, Both"]
    petSizeAccepted = ["small", "Medium", "Large"]
    ageRange = ["Puppy", "Adult", "Senior"]
    specialNeedsAndMedicalPetsAccepted = True

class Certification:
    id = Column(Integer, primary_key=True, index=True)
    certificationName = ""
    certificationDescription = ""
    certificationUrl = ""

class ServiceOffer:
    id = Column(Integer, primary_key=True, index=True)
    servicesName = ""
    servicePrice = ""
    pricingBasis = ["Per hour", "Per day", "Per session"]
    description = ""

class ImageGallery:
    id = Column(Integer, primary_key=True, index=True)
    imageUrl = ""
    name = ""

class ReviewsAndRating:
    id = Column(Integer, primary_key=True, index=True)
    starRating = 5
    reviewTitle = "Wonderful stay!"
    reviewText = "The host took great care of my dog. Highly recommended!"
    createAt = ""
    updatedAt = ""

