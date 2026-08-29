import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def generate_explanation(
    action: str,
    recovery_probability: float,
    expected_recovery_value: float,
    failure_reason: str,
    retry_count: int,
) -> dict:
    prompt = f"""You are explaining an automated payment recovery decision to a merchant.

Facts:
- Selected action: {action}
- Recovery probability: {recovery_probability:.2f}
- Expected recovery value: {expected_recovery_value:.2f}
- Failure reason: {failure_reason}
- Prior retry attempts: {retry_count}

Write a concise, 1-2 sentence explanation of why this action was selected,
in plain business language. Do not mention probabilities as raw decimals -
describe them qualitatively (e.g. "high", "moderate", "low"). Respond with
ONLY the explanation text, no preamble, no quotes."""

    try:
        client = get_client()
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        explanation = response.text.strip()
        return {
            "explanation": explanation,
            "source": "llm",
        }
    except Exception as e:
        fallback_explanation = (
            f"Action '{action}' was selected based on a recovery probability "
            f"of {recovery_probability:.0%} and an expected recovery value of "
            f"{expected_recovery_value:.2f}, given failure reason "
            f"'{failure_reason}' and {retry_count} prior attempt(s)."
        )
        return {
            "explanation": fallback_explanation,
            "source": "fallback",
            "error": str(e),
        }
