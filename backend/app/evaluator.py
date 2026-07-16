from typing import Dict, Any, List

def evaluate_submission(user_answers: Dict[str, Any], expected: Dict[str, Any]) -> Dict:
    """
    Returns: {
        score: int,
        feedback: { errors: List[str], explanations: List[str], recommendations: List[str] }
    }
    """
    score = 100
    errors = []
    explanations = []
    recommendations = []

    # Pre‑defined field‑specific help (can be extended)
    field_help = {
        "grossProfit": "Gross Profit = Revenue – Cost of Goods Sold (50,000 – 30,000 = 20,000).",
        "netIncome": "Net Income is given as 10,000 in this scenario – you should match the stated figure."
    }

    for field, correct_value in expected.items():
        user_val = user_answers.get(field)
        if user_val == correct_value:
            explanations.append(f"✅ {field} is correct ({correct_value}).")
        else:
            score -= 20
            errors.append(f"❌ {field}: expected {correct_value}, got {user_val}.")
            # Provide explanation if available
            if field in field_help:
                explanations.append(f"💡 {field_help[field]}")
            else:
                explanations.append(f"💡 Please check the calculation for {field}.")

    # Global recommendations
    if score < 100:
        recommendations.append("Review the standard formula: Revenue - COGS = Gross Profit.")
        recommendations.append("Double‑check the given values before submitting.")
    else:
        recommendations.append("Excellent work! Your calculations are spot on.")

    # Clamp score
    score = max(0, score)

    return {
        "score": score,
        "feedback": {
            "errors": errors,
            "explanations": explanations,
            "recommendations": recommendations
        }
    }