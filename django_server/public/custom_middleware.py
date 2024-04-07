from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from utils.secret_key import check_token
from public.status_code import TOKEN_Missing_Token


# class JwtUrlAuthentication(BaseAuthentication):
#
#     def authenticate(self, request: Request) -> tuple[dict, str]:
#         token: str | None = request.query_params.get('token', None)
#         if not token:
#             raise AuthenticationFailed(TOKEN_Missing_Token)
#         account, status = check_token(token)
#         if not status:
#             raise AuthenticationFailed(account)
#         return account, token
#
#     def authenticate_header(self, request):
#         return "API"


class JwtHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[dict, str]:
        token: str = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise AuthenticationFailed(TOKEN_Missing_Token)
        user, status = check_token(token)
        if not status:
            raise AuthenticationFailed(user)
        request.user_uuid = user.get("uuid", None)
        return user, token

    def authenticate_header(self, request):
        return "API"


class NoAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        token: str = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise AuthenticationFailed(TOKEN_Missing_Token)

    def authenticate_header(self, request):
        return "API"
