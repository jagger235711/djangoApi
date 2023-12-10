from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.versioning import QueryParameterVersioning


# Create your views here.
class HomeView(APIView):
    versioning_class = QueryParameterVersioning

    def get(self, request, format=None):
        print(request.version)
        print(request.versioning_scheme.reverse("order", request=request))
        return Response({"message": "Hello, world!"})
