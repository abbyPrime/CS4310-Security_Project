from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login, register, upload
import os

app = FastAPI(title="CinemaShare API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "CinemaShare API",
        "version": "1.0.0",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

app.include_router(login.router, prefix="/api")
app.include_router(register.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
