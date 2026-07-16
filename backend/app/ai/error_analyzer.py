
class ErrorAnalyzer:
    """detect error type"""
   
    def analyze(self, field, student_value, correct_value):

        if student_value == "" or student_value is None:

            return {

                "field": field,

                "error_type": f"Missing {field}",

                "severity": "High",

                "student_value": student_value,

                "correct_value": correct_value

            }

        calculation_fields = [

            "Gross Profit",

            "Net Income"

        ]

        if field in calculation_fields:

            return {

                "field": field,

                "error_type": f"Incorrect {field} Calculation",

                "severity": "High",

                "student_value": student_value,

                "correct_value": correct_value

            }

        return {

            "field": field,

            "error_type": f"Incorrect {field} Value",

            "severity": "Medium",

            "student_value": student_value,

            "correct_value": correct_value

        }