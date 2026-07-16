from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Case, Submission
from ..auth import get_current_user
from ..schemas import CaseOut, CaseDetailOut   # ← import CaseDetailOut

router = APIRouter(prefix="/api/cases", tags=["Cases"])

@router.get("/", response_model=list[CaseOut])
async def list_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    all_cases = db.query(Case).order_by(Case.id).all()
    submissions = db.query(Submission).filter(Submission.user_id == current_user.id).all()
    completed_ids = {s.case_id for s in submissions}
    scores = {s.case_id: s.score for s in submissions}

    response = []
    for case in all_cases:
        status = "locked"
        if case.id == 1:
            status = "unlocked"
        elif case.id == 2 and 1 in completed_ids:
            status = "unlocked"
        response.append(CaseOut(
            id=case.id,
            title=case.title,
            description=case.description,
            level=case.level,
            status=status,
            score=scores.get(case.id)
        ))
    return response

# ---------- NEW ENDPOINT ----------
@router.get("/{case_id}/detail", response_model=CaseDetailOut)
async def get_case_detail(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Get user's best score for this case
    submission = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.case_id == case_id
    ).order_by(Submission.score.desc()).first()
    
    # Determine status (simplified: unlocked if case 1, or if case 2 and case1 completed)
    # You can reuse logic from list_cases or keep it simple
    status = "locked"
    if case_id == 1:
        status = "unlocked"
    elif case_id == 2:
        # check if case 1 completed
        sub1 = db.query(Submission).filter(
            Submission.user_id == current_user.id,
            Submission.case_id == 1
        ).first()
        if sub1:
            status = "unlocked"
    # For future cases, you can expand logic – or simply store prerequisites in DB.
    
    return CaseDetailOut(
        id=case.id,
        title=case.title,
        description=case.description,
        level=case.level,
        status=status,
        score=submission.score if submission else None,
        expected=case.expected   # the key for dynamic frontend
    )