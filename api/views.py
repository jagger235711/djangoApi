from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.versioning import (
    QueryParameterVersioning,
    URLPathVersioning,
    AcceptHeaderVersioning,
)
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework import serializers

from api import models


# Create your views here.
class HomeView(APIView):
    versioning_class = QueryParameterVersioning
    parser_classes = [JSONParser, FormParser]
    content_negotiation_class = DefaultContentNegotiation

    def get(self, request):
        print(request.version)
        print(request.versioning_scheme.reverse("order", request=request))
        return Response({"message": "Hello, world!"})

    def post(self, request):
        print(request.data, type(request.data))
        return Response({"message": "Hello, world!from post"})


class Home2View(APIView):
    versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        print(request.version)
        print(request.versioning_scheme.reverse("h2", request=request))
        return Response({"message": "Hello, world!H2"})


class Home3View(APIView):
    versioning_class = AcceptHeaderVersioning

    def get(self, request, *args, **kwargs):
        print(request.version)
        # print(request.versioning_scheme.reverse("h2", request=request))
        return Response({"message": "Hello, world!H2"})


class DepartSerializer(serializers.Serializer):
    title = serializers.CharField()
    count = serializers.IntegerField()


class DepartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Depart
        fields = "__all__"


class DepartView(APIView):
    def get(self, request, *args, **kwargs):
        querySet = models.Depart.objects.all()
        ser = DepartSerializer(querySet, many=True)
        context = {"status": True, "data": ser.data}
        return Response(context)

    def post(self, request, *args, **kwargs):
        querySet = models.Depart.objects.all()
        ser = DepartModelSerializer(querySet, many=True)
        context = {"status": True, "data": ser.data}
        return Response(context)


class UserSerializer(serializers.Serializer):
    title = serializers.CharField()
    count = serializers.IntegerField()


class UserModelSerializer(serializers.ModelSerializer):
    gender_test = serializers.CharField(source="get_gender_display")
    depart = serializers.CharField(source="depart.title")
    ctime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    MyFun = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo
        fields = "__all__"

    def get_MyFun(self, obj):
        return "hello"


class UserView(APIView):
    def get(self, request, *args, **kwargs):
        querySet = models.UserInfo.objects.all()
        ser = DepartSerializer(querySet, many=True)
        context = {"status": True, "data": ser.data}
        return Response(context)

    def post(self, request, *args, **kwargs):
        querySet = models.UserInfo.objects.all()
        ser = UserModelSerializer(querySet, many=True)
        context = {"status": True, "data": ser.data}
        return Response(context)
