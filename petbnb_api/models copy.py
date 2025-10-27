from database import Base
from sqlalchemy import Column, Integer, String, Float


class PetHost(Base):
    def __init__(self):
        self.userId = ""
        self.firstName = ""
        self.lastName = ""
        self.email = ""
        self.mobileNumber = []
        self.bio = ""
        self.experience = "1 Year"
        self.address = ""
        self.latitude = ""
        self.longitude = ""
        self.accountStatus = ['active', 'blocked', 'under_review']
        self.rating = 4.9
        self.profileImage = ""
        self.isVerified = True
        self.numberOfPetHosted = 0
        self.hosting_capacity = 0
        self.languages = ["English", "Hindi", "Marathi"]
        self.petPreferences = PetPreferences()
        self.certification = Certification()
        self.serviceOffer = ServiceOffer()
        self.imageGallery = ImageGallery()
        self.availabilityStatus = ["available", "unavailable", "on_leave"]
        self.isSuperhost = True
        self.total_reviews = 0
        self.createdAt = ""
        self.updatedAt = ""
        self.reviewsAndRating = []
        self.totalEarnings = ""


class PetPreferences:
    def __init__(self):
        self.petType = ["Dog, Cat, Both"]
        self.petSizeAccepted = ["small", "Medium", "Large"]
        self.ageRange = ["Puppy", "Adult", "Senior"]
        self.specialNeedsAndMedicalPetsAccepted = True

class Certification:
    def __init__(self):
        self.certificationName = ""
        self.certificationDescription = ""
        self.certificationUrl = ""

class ServiceOffer:
    def __init__(self):
        self.servicesName = ""
        self.servicePrice = ""
        self.pricingBasis = ["Per hour", "Per day", "Per session"]
        self.description = ""

class ImageGallery:
    def __init__(self):
        self.imageUrl = ""
        self.name = ""

class ReviewsAndRating:
    def __init__(self):
        self.starRating = 5
        self.reviewTitle = "Wonderful stay!"
        self.reviewText = "The host took great care of my dog. Highly recommended!"
        self.createAt = ""
        self.updatedAt = ""

