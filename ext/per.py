import random
from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    message = {"status": False, "msg": "无权访问1"}

    def has_permission(self, request, view):
        v1 = random.randint(1, 3)
        print("p1")
        if v1 == 2:
            return True
        return False


class MyPermission2(BasePermission):
    message = {"status": False, "msg": "无权访问2"}

    def has_permission(self, request, view):
        v1 = random.randint(1, 3)
        print("p2")
        if v1 == 2:
            return True
        return False


class MyPermission3(BasePermission):
    message = {"status": False, "msg": "无权访问3"}

    def has_permission(self, request, view):
        v1 = random.randint(1, 3)
        print("p3")
        if v1 == 2:
            return True
        return False
