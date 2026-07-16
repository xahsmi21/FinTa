from fastapi import APIRouter
from ai.evaluator import Evaluator
from ai.feedback_generator import FeedbackGenerator
from models.case import Case

router = APIRouter(prefix="/api", tags=["AI"])

@router.post("/evaluate")
def evaluate(student_sheet: dict):

    case = Case(
        case_id=1,
        title="Income Statement Practice",
        difficulty="Easy",
        revenue=50000,
        cogs=30000,
        operating_expenses=10000
    )

    evaluator = Evaluator()
    evaluation_result = evaluator.evaluate(student_sheet, case)

    generator = FeedbackGenerator()
    feedback = generator.generate(evaluation_result)

    return {
        "score": evaluation_result["score"],
        "errors": evaluation_result["errors"],
        "feedback": feedback
    }