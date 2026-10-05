import hashlib
import json
import os
import re
import time


class AIServiceError(Exception):
    """A safe, user-facing AI service failure."""


class AIProviderNotConfigured(AIServiceError):
    pass


# HTTP status codes that indicate a transient provider-side problem.
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
# HTTP status codes that indicate a configuration problem; retrying cannot help.
NON_RETRYABLE_STATUS_CODES = {400, 401, 403, 404}
RETRYABLE_KEYWORDS = (
    'UNAVAILABLE',
    'RESOURCE_EXHAUSTED',
    'HIGH DEMAND',
    'DEADLINE_EXCEEDED',
    'TIMEOUT',
    'BACKEND_ERROR',
)
NON_RETRYABLE_KEYWORDS = (
    'API_KEY_INVALID',
    'API KEY NOT VALID',
    'PERMISSION_DENIED',
    'NOT_FOUND',
    'INVALID_ARGUMENT',
)
# Seconds to wait before each retry attempt within a model.
BACKOFF_SCHEDULE = (1.5, 3.0)
DEFAULT_FALLBACK_MODELS = 'gemini-2.5-flash,gemini-2.0-flash'


def _status_code(exc):
    for attr in ('code', 'status_code', 'status'):
        value = getattr(exc, attr, None)
        if isinstance(value, int):
            return value
    return None


def _is_retryable(exc):
    """Return True when the failure is transient and worth another attempt."""
    code = _status_code(exc)
    if code in NON_RETRYABLE_STATUS_CODES:
        return False
    if code in RETRYABLE_STATUS_CODES:
        return True
    text = str(exc).upper()
    if any(keyword in text for keyword in NON_RETRYABLE_KEYWORDS):
        return False
    return any(keyword in text for keyword in RETRYABLE_KEYWORDS)

def _is_model_unavailable(exc):
    """True when this model cannot serve the request at all right now.

    Covers removed models (404) and exhausted daily quota (429 quota errors).
    Retrying the same model cannot help; the chain should move on.
    """
    code = _status_code(exc)
    if code == 404:
        return True
    text = str(exc).upper()
    return code == 429 and 'QUOTA' in text

def _cache_key(system_prompt, user_prompt, json_mode):
    payload = f'{system_prompt}\n{user_prompt}\njson={int(json_mode)}'
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


class AIProvider:
    """Gateway to the Gemini API.

    Resilience strategy, applied in order:
    1. Serve an identical previous prompt from the local response cache.
    2. Retry transient failures (503/429/timeouts) with a short backoff.
    3. Fall back to secondary models when the primary model is unavailable.
    4. Raise AIServiceError with a safe message when every attempt fails.
    """

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', '').strip()
        self.model = os.getenv('GEMINI_MODEL', 'gemini-3.6-flash').strip()
        fallback_raw = os.getenv('GEMINI_FALLBACK_MODELS', DEFAULT_FALLBACK_MODELS)
        self.fallback_models = [name.strip() for name in fallback_raw.split(',') if name.strip()]
        try:
            self.retry_attempts = max(1, int(os.getenv('AI_RETRY_ATTEMPTS', '2')))
        except ValueError:
            self.retry_attempts = 2
        self.cache_enabled = os.getenv('AI_RESPONSE_CACHE', 'true').strip().lower() in ('1', 'true', 'yes', 'on')
        self.last_model = self.model

    def model_order(self):
        order = [self.model]
        order.extend(name for name in self.fallback_models if name != self.model)
        return order

    def generate(self, system_prompt, user_prompt, json_mode=False):
        if not self.api_key:
            raise AIProviderNotConfigured(
                'AI is not configured yet. Add GEMINI_API_KEY to your environment and restart the server.'
            )
        key = _cache_key(system_prompt, user_prompt, json_mode)
        cached = self._cache_get(key)
        if cached is not None:
            return cached
        last_error = None
        for model in self.model_order():
            for attempt in range(self.retry_attempts):
                if attempt:
                    time.sleep(BACKOFF_SCHEDULE[min(attempt - 1, len(BACKOFF_SCHEDULE) - 1)])
                try:
                    content = self._call(model, system_prompt, user_prompt, json_mode)
                except Exception as exc:
                    if _is_model_unavailable(exc):
                        last_error = exc
                        break
                    if not _is_retryable(exc):
                        raise AIServiceError(f'AI provider request failed: {exc}') from exc
                    last_error = exc
                    continue  
                self.last_model = model
                self._cache_set(key, content, model)
                return content
        total = len(self.model_order()) * self.retry_attempts
        raise AIServiceError(f'AI provider request failed after {total} attempts: {last_error}')

    def _call(self, model, system_prompt, user_prompt, json_mode):
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=self.api_key)
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
            response_mime_type='application/json' if json_mode else None,
        )
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=config,
        )
        content = response.text or ''
        return content.strip()

    def _cache_get(self, key):
        if not self.cache_enabled:
            return None
        from ..models import AIResponseCache

        row = AIResponseCache.objects.filter(cache_key=key).first()
        return row.response if row else None

    def _cache_set(self, key, response, model):
        if not self.cache_enabled:
            return
        from ..models import AIResponseCache

        AIResponseCache.objects.update_or_create(
            cache_key=key,
            defaults={'response': response, 'model_name': model},
        )


def parse_json_response(text):
    """Parse strict JSON and tolerate providers that wrap JSON in a code fence."""
    candidate = text.strip()
    candidate = re.sub(r'^```(?:json)?\s*', '', candidate, flags=re.IGNORECASE)
    candidate = re.sub(r'\s*```$', '', candidate)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return {'raw': text}