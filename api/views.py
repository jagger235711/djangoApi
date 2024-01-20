from django.http import HttpResponse
from django.shortcuts import render
from api import models
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

# Create your views here.


def db(request):
    v1 = models.UserInfo.objects.create(username="wuwenjie", password="123")
    v2 = models.UserInfo.objects.create(username="jiruyi", password="123")

    models.Blog.objects.create(
        category=1,
        image="xxxx/xxxx.png",
        title="my blog",
        summary="....",
        text="asdfasfasgafsg",
        creator=v1,
    )
    models.Blog.objects.create(
        category=2,
        image="xxxx/xxxx.png",
        title="aaaaaaaaaaaaaaaaa",
        summary="....",
        text="我好牛逼",
        creator=v2,
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
