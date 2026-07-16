from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from ..database import get_db
from ..models import User, Case, Submission
from ..schemas import UserOut
from ..auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["User"])

class LevelUpdate(BaseModel):
    level: str  # "easy" or "medium"

@router.patch("/level", response_model=UserOut)
async def update_level(
    level_data: LevelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate level
    if level_data.level not in ["easy", "medium"]:
        raise HTTPException(
            status_code=400, 
            detail="Level must be 'easy' or 'medium'"
        )
    
    # Update user's level
    current_user.level = level_data.level
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.get("/report")
async def get_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_cases = db.query(Case).count()
    submissions = db.query(Submission).filter(Submission.user_id == current_user.id).all()
    completed = len(submissions)
    avg_score = round(sum(s.score for s in submissions) / completed) if completed > 0 else 0

    return {
        "averageScore": avg_score,
        "level": current_user.level,
        "completedCount": completed,
        "totalCases": total_cases
    }