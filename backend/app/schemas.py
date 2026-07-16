from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List

# --- Auth ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: str
    name: Optional[str]
    level: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# --- Cases ---
class CaseOut(BaseModel):
    id: int
    title: str
    description: str
    level: str
    status: str          # "unlocked" or "locked"
    score: Optional[int] = None

# ---------- NEW SCHEMA ----------
class CaseDetailOut(CaseOut):
    expected: Dict[str, Any]  # the expected answers

    class Config:
        from_attributes = True

# --- Submissions ---
class SubmissionCreate(BaseModel):
    case_id: int
    answers: Dict[str, Any]   # e.g., {"grossProfit": 20000, "netIncome": 10000}

class FeedbackOut(BaseModel):
    errors: List[str]
    explanations: List[str]
    recommendations: List[str]

class SubmissionResponse(BaseModel):
    score: int
    feedback: FeedbackOut