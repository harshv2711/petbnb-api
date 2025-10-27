# database.py
from sqlalchemy import create_engine, Column, Integer, Float, Boolean, String, DateTime, func, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import pytz
from datetime import datetime 
# Database URL (change creds as needed)
# DATABASE_URL = "postgresql://petbnb_user:petbnb@123@localhost:5432/petbnb_db"
DATABASE_URL = "sqlite:///sqlite.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base() 

class PetHost(Base):
    __tablename__ = "pet_hosts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    mobile_number = Column(String)
    bio = Column(String)
    exprience = Column(String)
    address = Column(String)
    account_status = Column(String, default="under_review")
    rating = Column(Integer, default=0)
    profile_image = Column(String)
    is_verified = Column(Boolean, default=False)
    number_of_pet_hosted = Column(Integer, default=0)
    hosting_capacity = Column(Integer, default=1)
    language = Column(String)
    availability_status = Column(String, default="available")
    is_superhost = Column(Boolean, default=False)
    total_review = Column(Integer, default=0)
    total_earnings = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class PetPreferences(Base):
    __tablename__ = "pet_preferences"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(ForeignKey,("pet_hosts.id"))
    pet_type = Column(String) # Dog, Cat, Both
    pet_size_accepted = Column(String) # Small, Medium, Large
    age_range = Column(String) # Puppy, Adult, Senior
    special_needs_pet_accepted = Column(Boolean, default=True)
    medical_needs_pet_accepted = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(ForeignKey,("pet_hosts.id"))
    certificate_name = Column(String)
    certificate_url = Column(String)
    certificate_description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class ServiceOffer(Base):
    __tablename__ = "service_offer"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(ForeignKey,("pet_hosts.id"))
    service_name = Column(String)
    service_description = Column(String)
    service_price = Column(Integer)
    pricing_basis = Column(String) # ["Per hour", "Per day", "Per session"]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class ImageGallery(Base):
    __tablename__ = "image_galleries"

    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(ForeignKey,("pet_hosts.id"))
    image_url = Column(String)
    image_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
class ReviewsAndRating(Base):
    __tablename__ = "reviews_and_rating"
    id = Column(Integer, primary_key=True, index=True)
    pet_host_id = Column(ForeignKey,("pet_hosts.id"))
    star_rating = Column(Integer, default=0)
    review_title = Column(String)
    review_text = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


Base.metadata.create_all(engine)