from .database import engine, SessionLocal
from .models import Case
from sqlalchemy import text

def seed():
    # Check if cases already exist
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM cases"))
        count = result.scalar()
        if count > 0:
            print("Cases already seeded.")
            return

    # Insert cases
    cases = [
        {
            "id": 1,
            "title": "Case 1: Income Statement",
            "description": "Practice calculating gross profit and net income.",
            "level": "Easy",
            "expected": {"grossProfit": 20000, "netIncome": 10000}
        },
        {
            "id": 2,
            "title": "Case 2: Balance Sheet",
            "description": "Balance assets, liabilities, and equity.",
            "level": "Medium",
            "expected": {"totalAssets": 150000, "totalLiabilities": 60000, "equity": 90000}
        }
    ]

    with SessionLocal() as session:
        for case_data in cases:
            case = Case(**case_data)
            session.add(case)
        session.commit()
        print("✅ Seeded 2 cases successfully!")

if __name__ == "__main__":
    seed()