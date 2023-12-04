import uuid
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from app01 import models

from ext.per import UserPermission, ManagerPermission, BossPermission

from ext.throttle import MyThrottle

# Create your views here.


# def auth(request):
#     return JsonResponse({"status": True, "message": "success"})


# class UserView(View):
#     def get(self, request, pk):
#         return JsonResponse(
#             {"status": True, "message": "success!im user-get", "pk": pk}
#         )

#     def post(self, request, *args, **kwargs):
#         return JsonResponse(
#             {
#                 "status": True,
#                 "message": "success!im user-post",
#                 "pk": kwargs.get("pk", 1),  # 默认值不能写成关键字参数的形式
#             }
#         )


# @api_view(["GET"])
# def login(request):
#     return Response({"status": True, "message": "success"})


# class InfoView(APIView):
#     # def get(self, request):
#     #     kwargs = self.kwargs
#     #     return Response(
#     #         {"status": True, "message": "success!im InfoView-get2", "kwargs": kwargs}
#     #     )

#     def get(self, request, dt):
#         return Response({"status": True, "message": "success-get", "dt": dt})

#     def post(self, request, *args, **kwargs):
#         return Response(
#             {"status": True, "message": "success-post", "dt": kwargs.get("dt", "nice!")}
#         )


# class AuthloginView(APIView):
#     # authentication_classes = []

#     def get(self, request):
#         return Response({"status": True, "message": "success-get AuthloginView"})


# class AuthuserView(APIView):
#     authentication_classes = [
#         MyAuthentication2,
#     ]

#     def get(self, request):
#         return Response({"status": True, "message": "success-get AuthuserView"})


# class AuthorderView(APIView):
#     authentication_classes = [
#         MyAuthentication2,
#     ]


#     def get(self, request):
#         return Response({"status": True, "message": "success-get AuthorderView"})
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [MyThrottle]

    def post(self, request):
        user = request.data.get("username")
        pwd = request.data.get("password")

        user_obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if not user_obj:
            return Response({"status": False, "message": "用户名或密码错误"})

        token = str(uuid.uuid4())
        user_obj.token = token
        user_obj.save()
        return Response({"status": True, "message": "success-post", "token": token})


class UserView(APIView):
    permission_classes = [UserPermission, ManagerPermission, BossPermission]

    def check_permissions(self, request):  # 修改权限认证为“或”关系
        for permission in self.get_permissions():
            if permission.has_permission(request, self):
                return
        else:
            self.permission_denied(
                request,
                message=getattr(permission, "message", None),
                code=getattr(permission, "code", None),
            )

    def post(self, request):
        return Response("UserView")


# from ext.per import MyPermission


class OrderView(UserView):
    permission_classes = [ManagerPermission, BossPermission]

    def check_permissions(self, request):  # 修改权限认证为“或”关系
        for permission in self.get_permissions():
            if permission.has_permission(request, self):
                return
        else:
            self.permission_denied(
                request,
                message=getattr(permission, "message", None),
                code=getattr(permission, "code", None),
            )

    def post(self, request):
        return Response("OrderView")


from rest_framework.request import Request


class AvatarView(UserView):
    permission_classes = [UserPermission, ManagerPermission]

    def post(self, request):
        return Response("AvatarView")

    def initialize_request(self, request, *args, **kwargs):
        super().initialize_request(request, *args, **kwargs)
        parser_context = self.get_parser_context(request)
        print("MyResuest")
        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context,
        )
