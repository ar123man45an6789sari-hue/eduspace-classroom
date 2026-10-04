import json
import os
import re


class AIServiceError(Exception):
    """A safe, user-facing AI service failure."""


class AIProviderNotConfigured(AIServiceError):
    pass


class AIProvider:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', '').strip()
        self.model = os.getenv('GEMINI_MODEL', 'gemini-3.6-flash').strip()

    def generate(self, system_prompt, user_prompt, json_mode=False):
        if not self.api_key:
            raise AIProviderNotConfigured(
                'AI is not configured yet. Add GEMINI_API_KEY to your environment and restart the server.'
            )
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3,
                response_mime_type='application/json' if json_mode else None,
            )
            response = client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=config,
            )
            content = response.text or ''
            return content.strip()
        except AIServiceError:
            raise
        except Exception as exc:
            raise AIServiceError(f'AI provider request failed: {exc}') from exc


def parse_json_response(text):
    """Parse strict JSON and tolerate providers that wrap it in a code fence."""
    candidate = text.strip()
    candidate = re.sub(r'^```(?:json)?\s*', '', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'\s*```$', '', candidate)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return {'raw': text}
