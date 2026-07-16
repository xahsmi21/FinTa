from .error_analyzer import ErrorAnalyzer

class Evaluator:
    def __init__(self):
        self.analyzer = ErrorAnalyzer()

    def evaluate(self, student_answers, correct_answers):
        """
        student_answers: dict from frontend (e.g., {"grossProfit": 20000})
        correct_answers: dict from database (e.g., {"grossProfit": 20000, "netIncome": 10000})
        """
        total_cells = len(correct_answers)
        correct_count = 0
        errors = []

        for field, correct_value in correct_answers.items():
            student_value = student_answers.get(field)

            if student_value == correct_value:
                correct_count += 1
            else:
                error = self.analyzer.analyze(
                    field,
                    student_value,
                    correct_value
                )
                errors.append(error)

        score = round((correct_count / total_cells) * 100, 2)

        return {
            "score": score,
            "errors": errors
        }