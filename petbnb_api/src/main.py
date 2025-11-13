# main.py
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.staticfiles import StaticFiles

from core.database import Base, engine
from routers import (
    petHostRouter,
    bookingRouter,
    petPreferenceRouter,
    petServiceRouter,
    petHostImageGalleryRouter,
    petProfileRouter,
)

# -----------------------------
# ⚙️ Settings
# -----------------------------
APP_TITLE = "MyPetBnB API"
APP_VERSION = "1.0.0"

# MEDIA ROOT (served under /media/*)
MEDIA_ROOT = os.path.abspath(os.environ.get("MEDIA_ROOT", "./media"))
os.makedirs(MEDIA_ROOT, exist_ok=True)

# CORS: allow local dev (Expo, emulators, LAN)
DEFAULT_CORS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8081",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://10.0.2.2:3000",  # Android emulator (web)
    "http://10.0.2.2:8000",  # Android emulator (API direct calls)
]
# Optionally override with EXPO_PUBLIC_CORS_ORIGINS="http://192.168.1.50:3000,http://192.168.1.50"
CORS_ORIGINS = [
    o.strip() for o in os.environ.get("EXPO_PUBLIC_CORS_ORIGINS", "").split(",") if o.strip()
] or DEFAULT_CORS

# -----------------------------
# 🧬 Lifespan (init/shutdown)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create DB tables on startup (basic dev flow; in prod use Alembic)
    Base.metadata.create_all(bind=engine)
    yield
    # teardown if needed

# -----------------------------
# 🚀 App
# -----------------------------
app = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan)

# GZip small responses too
app.add_middleware(GZipMiddleware, minimum_size=500)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if "*" not in CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 📂 Static /media
# -----------------------------
app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")
app.mount("/static/pets", StaticFiles(directory="pet_uploads"), name="pet_media")


# -----------------------------
# 🔌 Routers
# -----------------------------
app.include_router(petHostRouter)
app.include_router(bookingRouter)
app.include_router(petPreferenceRouter)
app.include_router(petServiceRouter)
app.include_router(petHostImageGalleryRouter)  # Image Gallery CRUD & uploads
app.include_router(petProfileRouter)

# -----------------------------
# 🌐 Utility endpoints
# -----------------------------
@app.get("/", tags=["meta"])
def home():
    return {"message": "PetBnB API is running 🚀", "version": APP_VERSION}

@app.get("/healthz", tags=["meta"])
def healthz():
    return {"ok": True}

@app.get("/config", tags=["meta"])
def config():
    # Safe, minimal introspection for debugging dev env
    return {
        "media_root": MEDIA_ROOT,
        "cors_origins": CORS_ORIGINS,
    }
