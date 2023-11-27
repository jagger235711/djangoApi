from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from app01 import models


class QueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token")
        if not token:
            return
        user_obj = models.UserInfo.objects.filter(token=token).first()
        if user_obj:
            return user_obj, token

    def authenticate_header(self, request):
        return "API"


class HeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            return
        user_obj = models.UserInfo.objects.filter(token=token).first()
        if user_obj:
            return user_obj, token

    def authenticate_header(self, request):
        return "API"


class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raise AuthenticationFailed({"status": False, "msg": "请登录"})

    def authenticate_header(self, request):
        return "API"
