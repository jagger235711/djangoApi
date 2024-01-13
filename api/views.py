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


class DpModelSerializer(serializers.ModelSerializer):
    # more = serializers.CharField(required=True)

    class Meta:
        model = models.Depart
        fields = "__all__"
        # extra_kwargs = {


class Dp2ModelSerializer(serializers.ModelSerializer):
    more = serializers.CharField(required=True)

    class Meta:
        model = models.Depart
        fields = ["order", "title", "count"]


class DpView(APIView):
    def post(self, request, *args, **kwargs):
        ser = DpModelSerializer(data=request.data)
        if ser.is_valid():
            instance = ser.save()
            xx = Dp2ModelSerializer(instance=instance)
            print(instance)
            return Response(xx.data)
        else:
            print(ser.errors)
            return Response(ser.errors)


class UuusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Depart
        fields = "__all__"


class UusModelSerializer(serializers.ModelSerializer):
    # more = serializers.CharField(required=True)
    gender_info = serializers.CharField(source="get_gender_display", read_only=True)
    v1 = serializers.SerializerMethodField()
    v2 = UuusModelSerializer(read_only=True, source="depart")

    class Meta:
        model = models.UserInfo
        fields = ["id", "name", "age", "depart", "gender", "gender_info", "v1", "v2"]
        extra_kwargs = {"id": {"read_only": True}, "gender": {"write_only": True}}

    def get_v1(self, obj):
        return {"v1": obj.id}


# class UusView(APIView):
#     def post(self, request, *args, **kwargs):
#         ser = UusModelSerializer(data=request.data)
#         if ser.is_valid():
#             instance = ser.save()
#             xx = UusModelSerializer(instance=instance)
#             print(instance)
#             return Response(xx.data)
#         else:
#             print(ser.errors)
#             return Response(ser.errors)
class UusView(APIView):
    def post(self, request, *args, **kwargs):
        ser = UusModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            print(ser.errors)
            return Response(ser.errors)


class NbField(serializers.IntegerField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        if self.method_name is None:
            self.method_name = "xget_{field_name}".format(field_name=field_name)
        super().bind(field_name, parent)

    def get_attribute(self, instance):
        method = getattr(self.parent, self.method_name)
        return method(instance)

    def to_representation(self, value):
        return str(value)


class NbModelSerializer(serializers.ModelSerializer):
    gender = NbField()

    class Meta:
        model = models.NbUserInfo
        fields = "__all__"
        extra_kwargs = {"age": {"write_only": True}}

    def xget_gender(self, obj):
        return obj.get_gender_display()


class NbView(APIView):
    def post(self, request, *args, **kwargs):
        ser = NbModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            print(ser.errors)
            return Response(ser.errors)
