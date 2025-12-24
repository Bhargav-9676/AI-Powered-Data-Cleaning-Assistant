import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user
from app.database import SessionLocal
from app.services.data_cleaning import analyze_csv, clean_csv
from app.utils.activity_logger import log_activity

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/clean-csv")
def upload_and_clean_csv(
    file: UploadFile = File(...),
    user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # -------------------------
    # SAVE FILE
    # -------------------------
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if os.path.getsize(file_path) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # LOG: UPLOAD
    log_activity(
        db,
        user_email,
        "UPLOAD",
        f"Uploaded file: {file.filename}"
    )

    # -------------------------
    # ANALYZE
    # -------------------------
    analysis = analyze_csv(file_path)

    log_activity(
        db,
        user_email,
        "ANALYZE",
        f"Rows: {analysis['total_rows']}, Columns: {analysis['total_columns']}"
    )

    # -------------------------
    # CLEAN
    # -------------------------
    cleaning_result = clean_csv(file_path)

    log_activity(
        db,
        user_email,
        "CLEAN",
        (
            f"Rows before: {cleaning_result['rows_before']}, "
            f"Rows after: {cleaning_result['rows_after']}, "
            f"Duplicates removed: {cleaning_result['duplicates_removed']}, "
            f"Missing values fixed: {cleaning_result['missing_values_fixed']}, "
            f"Quality score: {cleaning_result['data_quality_score']}"
        )
    )

    # -------------------------
    # RESPONSE (FIXED KEY)
    # -------------------------
    return {
        "analysis": analysis,
        "cleaning_summary": cleaning_result,
        "cleaning_steps": cleaning_result["steps"],   # ✅ FIXED HERE
        "cleaned_file_path": cleaning_result["cleaned_file_path"]
    }
