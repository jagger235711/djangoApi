from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token")
        if token:
            return ("jagger", token)
        else:
            raise AuthenticationFailed("认证失败，全局验证")


class MyAuthentication2(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token")
        if token:
            return ("jagger", token)
        else:
            raise AuthenticationFailed("认证失败，局部验证")