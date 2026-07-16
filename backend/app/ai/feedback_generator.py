from .prompt_builder import PromptBuilder
from .ai_service import AIService

class FeedbackGenerator:
    def __init__(self):
        self.builder = PromptBuilder()
        self.ai = AIService()

    def generate(self, evaluation_result):
        prompt = self.builder.build(evaluation_result)
        feedback_text = self.ai.generate(prompt)
        return feedback_text