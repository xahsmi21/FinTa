from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, TokenResponse, UserOut
from ..auth import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed = get_password_hash(user_data.password)
    
    # Create new user
    new_user = User(
        email=user_data.email,
        hashed_password=hashed,
        name=user_data.name,
        level="easy"  # Default level
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate token
    token = create_access_token({"sub": new_user.id})

    return TokenResponse(
        access_token=token,
        user=UserOut.model_validate(new_user)
    )
@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()

    # Verify password
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate token
    token = create_access_token({"sub": user.id})

    return TokenResponse(
        access_token=token,
        user=UserOut.model_validate(user)
    )