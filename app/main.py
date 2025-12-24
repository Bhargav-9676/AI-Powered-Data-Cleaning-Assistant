from fastapi import FastAPI

from app.database import engine, Base
from app import models  # IMPORTANT: registers all models
from app.routers import user_routes, pipeline_routes

# -------------------------
# APP INITIALIZATION
# -------------------------
app = FastAPI(
    title="AI Data Cleaning Assistant",
    version="1.0.0",
    description="An AI-powered pipeline for CSV analysis, cleaning, and quality scoring"
)

# -------------------------
# CREATE DATABASE TABLES
# -------------------------
Base.metadata.create_all(bind=engine)

# -------------------------
# INCLUDE ROUTERS
# -------------------------
app.include_router(user_routes.router)
app.include_router(pipeline_routes.router)

# -------------------------
# ROOT ENDPOINT
# -------------------------
@app.get("/")
def root():
    return {"message": "Server running successfully"}
