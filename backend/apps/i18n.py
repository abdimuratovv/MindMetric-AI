"""
Request language resolution. The product ships in exactly two languages —
Russian and Uzbek, no English — selected via the `X-Language` header the
frontend attaches to every request (frontend/src/api/client.js), with a
`?lang=` query param fallback for easy manual testing (e.g. Django admin
links, curl). Anything else (missing header, unsupported code) falls back
to DEFAULT_LANGUAGE rather than erroring, so a stale client never 500s.
"""

LANGUAGES = ('ru', 'uz')
DEFAULT_LANGUAGE = 'ru'


def get_language(request) -> str:
    lang = request.META.get('HTTP_X_LANGUAGE') or request.query_params.get('lang')
    return lang if lang in LANGUAGES else DEFAULT_LANGUAGE
