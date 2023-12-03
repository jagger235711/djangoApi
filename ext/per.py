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


class UserPermission(BasePermission):
    # 员工权限校验
    message = {"status": False, "msg": "非员工，无员工权限"}

    def has_permission(self, request, view):
        if request.user.role == 3:
            return True
        return False
class ManagerPermission(BasePermission):
    # 员工权限校验
    message = {"status": False, "msg": "非员工，无员工权限"}

    def has_permission(self, request, view):
        if request.user.role == 2:
            return True
        return False
class BossPermission(BasePermission):
    # 员工权限校验
    message = {"status": False, "msg": "非员工，无员工权限"}

    def has_permission(self, request, view):
        if request.user.role == 1:
            return True
        return False

