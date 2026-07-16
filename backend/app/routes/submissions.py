from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Case, Submission
from ..auth import get_current_user
from ..schemas import SubmissionCreate, SubmissionResponse, FeedbackOut
from ..ai import Evaluator, FeedbackGenerator

router = APIRouter(prefix="/api/submissions", tags=["Submissions"])

@router.post("/", response_model=SubmissionResponse)
async def submit_case(
    payload: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("🚀 Submission received")   # moved inside the function

    # Fetch case
    case = db.query(Case).filter(Case.id == payload.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # ----- AI EVALUATION -----
    print("📊 Starting evaluation...")
    evaluator = Evaluator()
    evaluation_result = evaluator.evaluate(payload.answers, case.expected)

    # ----- AI FEEDBACK GENERATION -----
    print("🤖 Generating AI feedback...")
    feedback_generator = FeedbackGenerator()
    try:
        ai_feedback_text = feedback_generator.generate(evaluation_result)
        print("✅ AI feedback received")
    except Exception as e:
        print(f"⚠️ Gemini AI error: {e}")
        ai_feedback_text = f"Score: {evaluation_result['score']}%. Please review your calculations."

    # Build structured feedback (store in DB)
    feedback = {
        "score": evaluation_result["score"],
        "errors": evaluation_result["errors"],
        "ai_feedback": ai_feedback_text
    }

    # Save submission
    submission = Submission(
        user_id=current_user.id,
        case_id=case.id,
        score=int(evaluation_result["score"]),
        answers=payload.answers,
        feedback=feedback
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Return structured response for frontend using AI feedback
    # Extract "Next Step" from AI feedback (optional)
    next_step = ""
    lines = ai_feedback_text.strip().split('\n')
    for i, line in enumerate(lines):
        if "Next Step:" in line and i + 1 < len(lines):
            next_step = lines[i + 1].strip()
            break
    if not next_step:
        next_step = "Review your calculations carefully."

    return {
        "score": int(evaluation_result["score"]),
        "feedback": {
            "errors": [e["error_type"] for e in evaluation_result["errors"]],
            "explanations": [ai_feedback_text],   # full AI feedback in this field
            "recommendations": [next_step]        # extracted next step
        }
    }