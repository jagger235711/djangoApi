from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import exceptions
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


# class DepartSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     count = serializers.IntegerField()


# class DepartModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Depart
#         fields = "__all__"


# class DepartView(APIView):
#     def get(self, request, *args, **kwargs):
#         querySet = models.Depart.objects.all()
#         ser = DepartSerializer(querySet, many=True)
#         context = {"status": True, "data": ser.data}
#         return Response(context)

#     def post(self, request, *args, **kwargs):
#         querySet = models.Depart.objects.all()
#         ser = DepartModelSerializer(querySet, many=True)
#         context = {"status": True, "data": ser.data}
#         return Response(context)


class UserSerializer(serializers.Serializer):
    title = serializers.CharField()
    count = serializers.IntegerField()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class UserModelSerializer(serializers.ModelSerializer):
    gender_test = serializers.CharField(source="get_gender_display")
    depart = serializers.CharField(source="depart.title")
    ctime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # MyFunction = serializers.SerializerMethodField()
    # 嵌套
    tags = TagsSerializer(many=True)

    class Meta:
        model = models.UserInfo
        fields = "__all__"

    # def get_MyFunction(self, obj):
    #     queryset = obj.tags.all()
    #     # result = []
    #     # for tag in queryset:
    #     #     result.append({"id": tag.id, "caption": tag.caption})
    #     # 推导式
    #     result = [{"id": tag.id, "caption": tag.caption} for tag in queryset]
    #     return result


# class UserView(APIView):
#     def get(self, request, *args, **kwargs):
#         querySet = models.UserInfo.objects.all()
#         ser = DepartSerializer(querySet, many=True)
#         context = {"status": True, "data": ser.data}
#         return Response(context)

#     def post(self, request, *args, **kwargs):
#         querySet = models.UserInfo.objects.all()
#         ser = UserModelSerializer(querySet, many=True)
#         context = {"status": True, "data": ser.data}
#         return Response(context)

from django.core.validators import RegexValidator


class DepartSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, max_length=16, min_length=6)
    email = serializers.CharField(validators=[RegexValidator(r"\d+", message="请输入数字")])

    def validate_email(self, value):
        print(value)
        if len(value) > 6:
            raise exceptions.ValidationError("邮箱长度不能超过6位")
        return value

    def validate(self, attrs):
        raise exceptions.ValidationError("全局钩子，自定义错误")


class DepartModelSerializer(serializers.ModelSerializer):
    more = serializers.CharField(required=True)

    class Meta:
        model = models.Depart
        fields = "__all__"
        # extra_kwargs = {
        #     "title": {"max_length": 5, "min_length": 1},
        #     "order": {"min_value": 5},
        #     "count": {"validators": [RegexValidator(r"\d+", message="请输入数字")]},
        # }


class DepartView(APIView):
    def get(self, request, *args, **kwargs):
        # 1.获取原始数据
        # 2.校验
        ser = DepartModelSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
            ser.validated_data.pop("more")
            print(ser.validated_data)
            ser.save()
        else:
            print(ser.errors)
        # ser.is_valid(raise_exception=True)
        # print(ser.validated_data)
        return Response("...")

    def post(self, request, *args, **kwargs):
        # 1.获取原始数据
        # 2.校验
        ser = DepartSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)
        # ser.is_valid(raise_exception=True)
        # print(ser.validated_data)
        return Response("...")


class UsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["gender", "name", "age", "depart", "tags"]

    def validate_depart(self, value):
        print(value)
        if value.id > 1:
            return value
        else:
            raise serializers.ValidationError("部门不存在")


class UsView(APIView):
    def post(self, request, *args, **kwargs):
        # 1.获取原始数据
        # 2.校验
        ser = UsModelSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
            ser.save()
        else:
            print(ser.errors)
        # ser.is_valid(raise_exception=True)
        # print(ser.validated_data)
        return Response("...")
