# Agents

This folder contains DSPy agent modules used by the API.

## Conventions
- Place agent files under `src/agents/`.
- Use `snake_case` filenames like `*_agents.py`.
- Each file should export a single `Agent` class.
- `Agent.forward` should return a `dspy.Prediction`.

## Recommended structure
1) Define a `dspy.Signature` with explicit `InputField` / `OutputField` descriptions.
2) In `Agent.__init__`, set up the LM and predictor.
3) In `Agent.forward`, call the predictor inside `dspy.settings.context(lm=...)`.

## Context
Load shared instructions from `context/system_prompt.md` using:

```python
from utils.context_loader import build_context_bundle
system_prompt = build_context_bundle("system_prompt.md")
```

## Minimal example

```python
import dspy
from utils.context_loader import build_context_bundle

class ExampleSignature(dspy.Signature):
    """Generate a concise answer."""
    system: str = dspy.InputField(desc="System prompt")
    user: str = dspy.InputField(desc="User input")
    answer: str = dspy.OutputField(desc="Final response")

class Agent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.ChainOfThought(ExampleSignature)
        self.model = dspy.LM("openai/gpt-5.1")
        self.system_prompt = build_context_bundle("system_prompt.md")

    def forward(self, text: str) -> dspy.Prediction:
        with dspy.settings.context(lm=self.model):
            result = self.predictor(system=self.system_prompt, user=text)
        return dspy.Prediction(text=result.answer)
```
