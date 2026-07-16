from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import auth, user, cases, submissions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FinTa Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development sat it '*'
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(cases.router)
app.include_router(submissions.router)

@app.get("/")
async def root():
    return {"message": "FinTa Auth Service is running"}