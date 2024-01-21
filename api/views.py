from django.http import HttpResponse
from django.shortcuts import render
from api import models
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

# Create your views here.


def db(request):
    # v1 = models.UserInfo.objects.create(username="wuwenjie", password="123")
    # v2 = models.UserInfo.objects.create(username="jiruyi", password="123")

    # models.Blog.objects.create(
    #     category=1,
    #     image="xxxx/xxxx.png",
    #     title="my blog",
    #     summary="....",
    #     text="asdfasfasgafsg",
    #     creator=v1,
    # )
    # models.Blog.objects.create(
    #     category=2,
    #     image="xxxx/xxxx.png",
    #     title="aaaaaaaaaaaaaaaaa",
    #     summary="....",
    #     text="我好牛逼",
    #     creator=v2,
    # )
    models.Comment.objects.create(
        blog_id=1,
        user_id=1,
        content="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    )
    models.Comment.objects.create(
        blog_id=1,
        user_id=2,
        content="jry!!!",
    )
    return HttpResponse("ok")


class BlogSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d")
    creator = serializers.SerializerMethodField()

    class Meta:
        model = models.Blog
        # fields = "__all__"
        fields = [
            "category",
            "image",
            "title",
            "summary",
            "ctime",
            "comment_count",
            "favor_count",
            "creator",
        ]

    def get_creator(self, obj):
        return {"username": obj.creator.username, "id": obj.creator.id}


class BlogView(APIView):
    def get(self, request, *args, **kwargs):
        """获取博客列表"""
        querySet = models.Blog.objects.all().order_by("-id")
        ser = BlogSerializer(instance=querySet, many=True)
        context = {"code": 200, "msg": "ok", "data": ser.data}
        return Response(context)

    # def post(self, request, *args, **kwargs):
    #     blog = models.Blog.objects.create(**request.data)
    #     return Response(blog.values())


class BlogDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d")
    creator = serializers.SerializerMethodField()

    class Meta:
        model = models.Blog
        fields = "__all__"
        # fields = [
        #     "category",
        #     "image",
        #     "title",
        #     "summary",
        #     "ctime",
        #     "comment_count",
        #     "favor_count",
        #     "creator",
        # ]

    def get_creator(self, obj):
        return {"username": obj.creator.username, "id": obj.creator.id}


class BlogDetailView(APIView):
    def get(self, request, *args, **kwargs):
        """获取博客详情"""
        pk = kwargs.get("pk")
        instance = models.Blog.objects.filter(id=pk).first()
        if not instance:
            return Response({"code": 400, "msg": "not found"})
        ser = BlogDetailSerializer(instance=instance, many=False)
        context = {"code": 200, "msg": "ok", "data": ser.data}
        return Response(context)


from ext.hook import HookSerializer


class CommentSerializer(HookSerializer, serializers.ModelSerializer):
    # user = serializers.CharField(source="user.username")

    class Meta:
        model = models.Comment
        fields = ["id", "content", "user"]

    def sb_user(self, obj):
        return {"username": obj.user.username, "id": obj.user.id}


class CommentView(APIView):
    def get(self, request, *args, **kwargs):
        """获取博客详情"""
        blog_id = kwargs.get("blog_id")
        querySet = models.Comment.objects.filter(blog_id=blog_id)
        ser = CommentSerializer(instance=querySet, many=True)
        context = {"code": 200, "msg": "ok", "data": ser.data}
        return Response(context)


class RegisterSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source="user.username")
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = models.UserInfo
        # 字段执行顺序与fields定义顺序一致
        fields = ["id", "username", "password", "confirm_password"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate_confirm_password(self, value):
        password = self.initial_data.get("password")
        if password != value:
            raise serializers.ValidationError("密码不一致")
        return value


class RegisterView(APIView):
    # def get(self, request, *args, **kwargs):
    #     """获取博客详情"""
    #     pk = kwargs.get("pk")
    #     instance = models.Blog.objects.filter(id=pk).first()
    #     if not instance:
    #         return Response({"code": 400, "msg": "not found"})
    #     ser = BlogDetailSerializer(instance=instance, many=False)
    #     context = {"code": 200, "msg": "ok", "data": ser.data}
    #     return Response(context)
    def post(self, request, *args, **kwargs):
        """注册"""
        ser = RegisterSerializer(data=request.data)
        if not ser.is_valid():
            content = {"code": 400, "msg": "注册失败", "data": ser.errors}
        else:
            # 排除不到保存的字段
            ser.validated_data.pop("confirm_password")
            ser.save()
            content = {"code": 200, "msg": "ok", "data": ser.data}
        return Response(content)
