import dspy

from utils.context_loader import build_context_bundle


class ReviseSignature(dspy.Signature):
    """Revise a previous output based on a new instruction."""

    system: str = dspy.InputField(desc="System prompt that defines behavior and constraints.")
    user: str = dspy.InputField(desc="Original user input or task context.")
    instruction: str = dspy.InputField(desc="Revision instruction from the user.")
    base: str = dspy.InputField(desc="Base output to revise.")
    revised: str = dspy.OutputField(desc="Revised output.")


class Agent(dspy.Module):
    def __init__(self, model: str | None = None):
        super().__init__()
        self.predictor = dspy.ChainOfThought(ReviseSignature)
        model_name = model or "openai/gpt-5.1"
        self.model = dspy.LM(model_name)
        self.system_prompt = build_context_bundle("system_prompt.md")

    def forward(
        self,
        text: str,
        instruction: str,
        base: str = "",
    ) -> dict:
        with dspy.settings.context(lm=self.model):
            result = self.predictor(
                system=self.system_prompt,
                user=text,
                instruction=instruction,
                base=base,
            )
        return {
            "text": (result.revised or "").strip(),
            "reasoning": (result.reasoning or "").strip(),
        }
