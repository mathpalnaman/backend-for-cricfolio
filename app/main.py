import os
from fastapi import FastAPI
from app.routers import contact
from fastapi.staticfiles import StaticFiles
from app.routers import tournament_router
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database.database import engine
from app.database.database import Base

print("Attempting to create tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("Tables checked/created successfully.")
except Exception as e:
    print(f"Error creating tables: {e}")


app = FastAPI(
     title="CricFolio API",
     description="API for managing cricket tournaments and players.",
     version="0.1.0",
)

# Ensure upload directory exists
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
print(f"Upload directory set to: {os.path.abspath(UPLOAD_DIR)}")


# CORS Middleware (already configured)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static Files ---
# Mount the directory specified by UPLOAD_DIR to serve banners
# The path "/static/banners" MUST match BANNER_URL_PREFIX in the router
app.mount("/static/banners", StaticFiles(directory=UPLOAD_DIR), name="banners")
print(f"Serving static files from '{UPLOAD_DIR}' at '/static/banners'")


# Include API Routers
app.include_router(contact.router)
app.include_router(tournament_router.router) # Include the tournament router


@app.get("/")
def read_root():
    return {"message": "CricFolio Backend running"}
