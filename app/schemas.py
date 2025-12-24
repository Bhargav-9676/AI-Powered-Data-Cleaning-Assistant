from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# -------------------------
# USER SCHEMAS
# -------------------------
class UserRegister(BaseModel):
    email: EmailStr
    password: str


# ⚠️ NOTE:
# This is kept only for frontend validation / documentation.
# Actual login uses OAuth2PasswordRequestForm (form-data).
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -------------------------
# FILE RESPONSE SCHEMA
# -------------------------
class FileResponse(BaseModel):
    original_filename: str
    stored_path: str
    uploaded_at: datetime


# -------------------------
# CLEANING RESULT SCHEMA
# -------------------------
class CleaningResult(BaseModel):
    rows_before: int
    rows_after: int
    duplicates_removed: int
    missing_values_fixed: int
    data_quality_score: int
    cleaned_file_path: str


# -------------------------
# CLEANING HISTORY SCHEMA
# -------------------------
class CleaningHistoryResponse(BaseModel):
    id: int
    rows_before: int
    rows_after: int
    duplicates_removed: int
    missing_values_fixed: int
    data_quality_score: int
    cleaned_file_path: str
    cleaned_at: datetime
