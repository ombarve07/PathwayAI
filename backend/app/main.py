import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.config import settings
from backend.app.seed import seed_database
from backend.app.routes import (
    auth, students, careers, assessments, recommendations, progress, payments, admin
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-seed database with all 30 careers, roadmaps, questions, and default admin on startup
    seed_database()
    yield

app = FastAPI(
    title="PATHWAY AI - Discover Your Potential. Build Your Future.",
    description="AI-powered career guidance and skill development platform tailored for Indian students.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(careers.router)
app.include_router(assessments.router)
app.include_router(recommendations.router)
app.include_router(progress.router)
app.include_router(payments.router)
app.include_router(admin.router)

# Mount Static Frontend
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/frontend", StaticFiles(directory=frontend_dir, html=True), name="frontend_dir")
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

