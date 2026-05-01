import os
from typing import Any, Dict

# Optional: import Anthropic SDK if available
try:
    from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
except Exception:  # pragma: no cover
    Anthropic = None
    HUMAN_PROMPT = "\n\nHuman:"
    AI_PROMPT = "\n\nAssistant:"


class LegalAgent:
    """Simple agent that generates legal policy text using Claude.

    The agent expects a ``policy_type`` (e.g. "terms", "privacy", "cookies")
    and an optional ``context`` dictionary that can be interpolated into the
    prompt. If the Anthropic SDK is not installed, it raises a clear error.
    """

    def __init__(self, api_key: str | None = None, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set to use LegalAgent")
        if Anthropic is None:
            raise ImportError("anthropic SDK not installed. Install with 'pip install anthropic'.")
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def _build_prompt(self, policy_type: str, context: Dict[str, Any] | None = None) -> str:
        base_prompt = (
            "You are a legal drafting expert. Write a concise, clear, and legally compliant "
            f"{policy_type} document for a SaaS platform called Mapgenius Solutions. "
            "Use plain language in Spanish. Include typical sections for this type of policy."
        )
        if context:
            # Simple key/value interpolation
            for k, v in context.items():
                base_prompt += f"\n- {k}: {v}"
        return base_prompt

    def generate(self, policy_type: str, context: Dict[str, Any] | None = None) -> str:
        """Generate the requested legal policy.

        Args:
            policy_type: Identifier such as "terms", "privacy", "cookies".
            context: Optional dictionary with values to be included.
        Returns:
            The generated policy text.
        """
        prompt = self._build_prompt(policy_type, context)
        response = self.client.completions.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.2,
            prompt=HUMAN_PROMPT + "\n" + prompt + AI_PROMPT,
        )
        # The SDK returns a Completion object; the generated text is in .completion
        return response.completion.strip()
