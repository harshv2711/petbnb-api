# # database.py
# from sqlalchemy import (
#     create_engine, Column, Integer, Float, Boolean, String,
#     DateTime, func, ForeignKey
# )
# from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# DATABASE_URL = "sqlite:///sqlite.db"
# engine = create_engine(DATABASE_URL, future=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# class PetHost(Base):
#     __tablename__ = "pet_hosts"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String)
#     first_name = Column(String)
#     last_name = Column(String)
#     email = Column(String)
#     mobile_number = Column(String)
#     bio = Column(String)
#     experience = Column(String)
#     address = Column(String)
#     account_status = Column(String, default="under_review")
#     rating = Column(Integer, default=0)
#     profile_image = Column(String)
#     is_verified = Column(Boolean, default=False)
#     number_of_pet_hosted = Column(Integer, default=0)
#     hosting_capacity = Column(Integer, default=1)
#     language = Column(String)
#     availability_status = Column(String, default="available")
#     is_superhost = Column(Boolean, default=False)
#     total_review = Column(Integer, default=0)
#     total_earnings = Column(Float, default=0.0)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

#     # -------- Relationships (attached collections/objects) --------
#     pet_preferences = relationship(
#         "PetPreferences",
#         back_populates="pet_host",
#         uselist=False,            # one-to-one
#         cascade="all, delete-orphan",
#         lazy="joined"             # grab with the host (1:1 is cheap to join)
#     )
#     certifications = relationship(
#         "Certification",
#         back_populates="pet_host",
#         cascade="all, delete-orphan",
#         lazy="selectin"           # efficient one-to-many loading
#     )
#     service_offers = relationship(
#         "ServiceOffer",
#         back_populates="pet_host",
#         cascade="all, delete-orphan",
#         lazy="selectin"
#     )
#     image_gallery = relationship(
#         "ImageGallery",
#         back_populates="pet_host",
#         cascade="all, delete-orphan",
#         lazy="selectin"
#     )
#     reviews = relationship(
#         "ReviewsAndRating",
#         back_populates="pet_host",
#         cascade="all, delete-orphan",
#         lazy="selectin"
#     )


# class PetPreferences(Base):
#     __tablename__ = "pet_preferences"

#     id = Column(Integer, primary_key=True, index=True)
#     pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), unique=True, nullable=False)
#     pet_type = Column(String)           # Dog, Cat, Both
#     pet_size_accepted = Column(String)  # Small, Medium, Large
#     age_range = Column(String)          # Puppy, Adult, Senior
#     special_needs_pet_accepted = Column(Boolean, default=True)
#     medical_needs_pet_accepted = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

#     pet_host = relationship("PetHost", back_populates="pet_preferences")


# class Certification(Base):
#     __tablename__ = "certifications"

#     id = Column(Integer, primary_key=True, index=True)
#     pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)
#     certificate_name = Column(String)
#     certificate_url = Column(String)
#     certificate_description = Column(String)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

#     pet_host = relationship("PetHost", back_populates="certifications")


# class ServiceOffer(Base):
#     __tablename__ = "service_offer"

#     id = Column(Integer, primary_key=True, index=True)
#     pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)
#     service_name = Column(String)
#     service_description = Column(String)
#     service_price = Column(Float)
#     pricing_basis = Column(String)  # "Per hour" | "Per day" | "Per session"
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

#     pet_host = relationship("PetHost", back_populates="service_offers")

# class ImageGallery(Base):
#     __tablename__ = "image_galleries"

#     id = Column(Integer, primary_key=True, index=True)
#     pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)
#     image_url = Column(String)
#     image_name = Column(String)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

#     pet_host = relationship("PetHost", back_populates="image_gallery")


# class ReviewsAndRating(Base):
#     __tablename__ = "reviews_and_rating"

#     id = Column(Integer, primary_key=True, index=True)
#     pet_host_id = Column(Integer, ForeignKey("pet_hosts.id"), nullable=False)
#     star_rating = Column(Integer, default=0)
#     review_title = Column(String)
#     review_text = Column(String)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

#     pet_host = relationship("PetHost", back_populates="reviews")


# Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
