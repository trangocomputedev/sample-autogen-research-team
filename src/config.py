import os
from autogen_ext.models.openai import OpenAIChatCompletionClient


def get_client(model: str = "gpt-4o") -> OpenAIChatCompletionClient:
    """Return a configured OpenAI model client."""
    return OpenAIChatCompletionClient(
        model=model,
        api_key=os.environ["OPENAI_API_KEY"],
    )
