import dspy

from utils.context_loader import build_context_bundle


class GenerateSignature(dspy.Signature):
    """Generate a helpful response to the user."""

    system: str = dspy.InputField(
        desc="System prompt that defines behavior and constraints."
    )
    user: str = dspy.InputField(desc="User input or task description.")
    answer: str = dspy.OutputField(desc="Final response to show the user.")


class Agent(dspy.Module):
    def __init__(self, model: str | None = None):
        super().__init__()
        self.predictor = dspy.ChainOfThought(GenerateSignature)
        model_name = model or "openai/gpt-5.1"
        self.model = dspy.LM(model_name)
        self.system_prompt = build_context_bundle("system_prompt.md")

    def forward(self, text: str) -> dspy.Prediction:
        with dspy.settings.context(lm=self.model):
            result = self.predictor(
                system=self.system_prompt,
                user=text,
            )
        return dspy.Prediction(
            text=result.answer,
            reasoning=result.reasoning,
        )
