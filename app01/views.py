from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from ext.auth import MyAuthentication2

# Create your views here.


def auth(request):
    return JsonResponse({"status": True, "message": "success"})


class UserView(View):
    def get(self, request, pk):
        return JsonResponse(
            {"status": True, "message": "success!im user-get", "pk": pk}
        )

    def post(self, request, *args, **kwargs):
        return JsonResponse(
            {
                "status": True,
                "message": "success!im user-post",
                "pk": kwargs.get("pk", 1),  # 默认值不能写成关键字参数的形式
            }
        )


@api_view(["GET"])
def login(request):
    return Response({"status": True, "message": "success"})


class InfoView(APIView):
    # def get(self, request):
    #     kwargs = self.kwargs
    #     return Response(
    #         {"status": True, "message": "success!im InfoView-get2", "kwargs": kwargs}
    #     )

    def get(self, request, dt):
        return Response({"status": True, "message": "success-get", "dt": dt})

    def post(self, request, *args, **kwargs):
        return Response(
            {"status": True, "message": "success-post", "dt": kwargs.get("dt", "nice!")}
        )


class AuthloginView(APIView):
    # authentication_classes = []

    def get(self, request):
        return Response({"status": True, "message": "success-get AuthloginView"})


class AuthuserView(APIView):
    authentication_classes = [
        MyAuthentication2,
    ]

    def get(self, request):
        return Response({"status": True, "message": "success-get AuthuserView"})


class AuthorderView(APIView):
    authentication_classes = [
        MyAuthentication2,
    ]

    def get(self, request):
        return Response({"status": True, "message": "success-get AuthorderView"})
