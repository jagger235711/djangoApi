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
