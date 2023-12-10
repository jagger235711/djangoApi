from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning


# Create your views here.
class HomeView(APIView):
    versioning_class = QueryParameterVersioning

    def get(self, request):
        print(request.version)
        print(request.versioning_scheme.reverse("order", request=request))
        return Response({"message": "Hello, world!"})


class Home2View(APIView):
    versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        print(request.version)
        print(request.versioning_scheme.reverse("h2", request=request))
        return Response({"message": "Hello, world!H2"})
