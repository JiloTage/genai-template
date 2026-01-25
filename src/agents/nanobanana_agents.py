from typing import Iterable
import os

import dspy

from image_models import FalAIClient

BASE_PROMPT = ""
MODEL = "fal-ai/nano-banana-pro/edit"


class Agent(dspy.Module):
    def __init__(self, *, base_prompt: str = BASE_PROMPT, **default_arguments):
        super().__init__()
        api_key = os.getenv("FAL_KEY")
        self.client = FalAIClient(MODEL, api_key=api_key)
        self.base_prompt = base_prompt
        self.default_arguments = default_arguments

    def forward(self, images: Iterable[str], prompt: str = ""):
        arguments = dict(self.default_arguments)
        full_prompt = (
            f"{self.base_prompt}\n{prompt}".strip() if prompt else self.base_prompt
        )
        image_urls = self.client.ensure_urls(images)
        result = self.client.generate(
            prompt=full_prompt, image_urls=image_urls, **arguments
        )
        return dspy.Prediction(result=result)
