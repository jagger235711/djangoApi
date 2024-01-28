import uuid
from django.http import HttpResponse
from django.shortcuts import render
from api import models
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

from ext.hook import HookSerializer

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


class BlogSerializer(HookSerializer, serializers.ModelSerializer):
    # category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Blog
        # fields = "__all__"
        fields = [
            "id",
            "category",
            "image",
            "title",
            "summary",
            "ctime",
            "comment_count",
            "favor_count",
            "creator",
            "text"
        ]
        extra_kwargs = {
            "comment_count": {"read_only": True},
            "favor_count": {"read_only": True},
            "text": {"write_only": True},
        }

    def get_creator(self, obj):
        return {"username": obj.creator.username, "id": obj.creator.id}

    def sb_category(self, obj):
        return obj.get_category_display()


class BlogView(APIView):
    def get(self, request, *args, **kwargs):
        """获取博客列表"""
        querySet = models.Blog.objects.all().order_by("-id")
        ser = BlogSerializer(instance=querySet, many=True)
        context = {"code": 200, "msg": "ok", "data": ser.data}
        return Response(context)

    def post(self, request, *args, **kwargs):
        # 新增博客
        if not request.user:
            context = {"code": 400, "msg": "用户未登录"}
            return Response(context)
        ser = BlogSerializer(data=request.data)
        if ser.is_valid():
            ser.save(creator=request.user)
            context = {"code": 200, "msg": "ok", "data": ser.data}
            return Response(context)
        else:
            context = {"code": 400, "msg": "fail", "data": ser.errors}
            return Response(context)


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


class CommentSerializer(HookSerializer, serializers.ModelSerializer):
    # user = serializers.CharField(source="user.username")

    class Meta:
        model = models.Comment
        fields = ["id", "content", "user"]
        extra_kwargs = {"id": {"read_only": True}, "user": {"read_only": True}}

    def sb_user(self, obj):
        return {"username": obj.user.username, "id": obj.user.id}


from ext.auth import BlogAuthentication, NoAuthentication


class CommentView(APIView):
    authentication_classes = [BlogAuthentication]

    def get(self, request, *args, **kwargs):
        """获取评论列表"""
        blog_id = kwargs.get("blog_id")
        querySet = models.Comment.objects.filter(blog_id=blog_id)
        ser = CommentSerializer(instance=querySet, many=True)
        context = {"code": 200, "msg": "ok", "data": ser.data}
        return Response(context)

    def post(self, request, *args, **kwargs):
        """创建评论"""
        if not request.user:
            return Response({"code": 400, "msg": "未登录"})
        blog_id = kwargs.get("blog_id")
        blog_object = models.Blog.objects.filter(id=blog_id).first()
        if not blog_object:
            return Response({"code": 400, "msg": "博客不存在"})
        ser = CommentSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"code": 400, "msg": "参数错误", "error": ser.errors})
        ser.save(user=request.user, blog=blog_object)
        return Response({"code": 200, "msg": "ok", "data": ser.data})


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


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        # 字段执行顺序与fields定义顺序一致
        fields = [
            "username",
            "password",
        ]


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        """登陆"""
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            content = {"code": 400, "msg": "校验失败", "errors": ser.errors}
            return Response(content)
        instance = models.UserInfo.objects.filter(**ser.validated_data).first()
        if not instance:
            return Response({"code": 400, "msg": "用户名或密码错误"})
        token = str(uuid.uuid4())
        instance.token = token
        instance.save()
        content = {"code": 200, "msg": "登陆成功", "token": instance.token}
        return Response(content)


class FavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favor
        # 字段执行顺序与fields定义顺序一致
        fields = ["blog"]


class FavorView(APIView):
    authentication_classes = [BlogAuthentication, NoAuthentication]

    def post(self, request, *args, **kwargs):
        # 先找博客是否存在
        ser = FavorSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"code": 400, "msg": "校验失败", "errors": ser.errors})
        # 再看该用户是否给这个博客点赞了
        exists = models.Favor.objects.filter(
            user=request.user, blog=ser.validated_data["blog"]
        ).exists()
        if exists:
            return Response({"code": 400, "msg": "已经点赞过了"})
        ser.save(user=request.user)
        return Response({"code": 200, "msg": "点赞成功", "data": ser.data})
