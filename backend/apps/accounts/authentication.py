from rest_framework_simplejwt.authentication import JWTAuthentication as SimpleJWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from apps.i18n import get_language

SESSION_REVOKED = {
    'ru': 'Сеанс завершён. Войдите снова.',
    'uz': 'Seans yakunlandi. Qaytadan kiring.',
}


class JWTAuthentication(SimpleJWTAuthentication):
    """
    simplejwt's authentication plus one check: a token issued before the user's
    `tokens_valid_after` is refused, which is how a password change or "sign out
    everywhere" (apps.accounts.views) ends sessions on other devices.

    `iat` is whole seconds, so the cutoff is floored to the second too: the fresh
    token those views hand back to the current session is issued in the same
    second as the cutoff and has to stay valid.
    """

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, token = result
        cutoff = user.tokens_valid_after
        if cutoff is not None and token.get('iat', 0) < int(cutoff.timestamp()):
            raise AuthenticationFailed(SESSION_REVOKED[get_language(request)], code='token_revoked')
        return result
